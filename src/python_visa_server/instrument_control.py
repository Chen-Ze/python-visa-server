import pyvisa
import json
import sys
from traceback import format_exc
import coloredlogs
import logging
import threading
from keithley2600 import Keithley2600
from keithley2600.keithley_driver import Keithley2600 as Keithley2600Controller
from pymeasure.instruments.keithley import Keithley2400
import python_visa_additional_control.lightfield.pi_lightfield as pi


logger = logging.getLogger("instrument_control")
logger.setLevel(logging.DEBUG)
logger.propagate = False

fileFormatter = coloredlogs.BasicFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
loggerFileHandler = logging.FileHandler('instrument.log')
loggerFileHandler.setLevel(logging.DEBUG)
loggerFileHandler.setFormatter(fileFormatter)
logger.addHandler(loggerFileHandler)

streamFormatter = coloredlogs.ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
loggerStreamHandler = logging.StreamHandler()
loggerStreamHandler.setLevel(logging.ERROR)
loggerStreamHandler.setFormatter(streamFormatter)
logger.addHandler(loggerStreamHandler)


STB_DATA_READY = 1

class InstrumentController:
    def __init__(self):
        self.mutex_lock = threading.Lock()
        self.rm = pyvisa.ResourceManager()
        self.instruments = { }
        self.model2400s  = { } # type: dict[str, Keithley2400]
        self.model2600s  = { } # type: dict[str, Keithley2600Controller]

    def list_resources(self):
        return self.rm.list_resources()

    def open_instrument(self, name, address):
        instrument = self.rm.open_resource(address)
        self.instruments[name] = instrument
        return { "instruments": str(self.instruments) }

    def open_model(self, name: str, address: str, model: str):
        if model == "Model2400":
            self.model2400s[name] = Keithley2400(address)
            return { "model2400s": str(self.model2400s) }
        if model == "Model2600":
            self.model2600s[name] = Keithley2600(address, visa_library='')
            return { "model2600s": str(self.model2600s) }

    def query_model(self, name: str, query, model: str):
        if model == "Model2400":
            controller = self.model2400s[name]
            if query["task"] == "set-smu-off":
                controller.shutdown()
                return { }
            elif query["task"] == "set-integration-time":
                return { }
            elif query["task"] == "set-smu-current-compliance":
                controller.compliance_current = float(query["value"])
                return { }
            elif query["task"] == "set-smu-voltage-compliance":
                controller.compliance_voltage = float(query["value"])
                return { }
            elif query["task"] == "set-smu-current":
                controller.apply_current()
                controller.source_current = float(query["value"])
                controller.enable_source()
                return { }
            elif query["task"] == "set-smu-voltage":
                controller.apply_voltage()
                controller.source_voltage = float(query["value"])
                controller.enable_source()
                return { }
            elif query["task"] == "measure-smu-voltage":
                controller.measure_voltage()
                return { "read": controller.voltage }
            elif query["task"] == "measure-smu-current":
                controller.measure_current()
                return { "read": controller.current }
        elif model == "Model2600":
            controller = self.model2600s[name]
            if query["task"] == "set-smua-off":
                controller.smua.source.output = controller.smua.OUTPUT_OFF
                return { }
            elif query["task"] == "set-smub-off":
                controller.smub.source.output = controller.smub.OUTPUT_OFF
                return { }
            elif query["task"] == "set-integration-time":
                controller.set_integration_time(controller.smua, float(query["value"]) * 0.001)
                controller.set_integration_time(controller.smub, float(query["value"]) * 0.001)
                return { }
            elif query["task"] == "set-smua-current-compliance":
                controller.smua.source.limiti = float(query["value"])
                return { }
            elif query["task"] == "set-smub-current-compliance":
                controller.smub.source.limiti = float(query["value"])
                return { }
            elif query["task"] == "set-smua-voltage-compliance":
                controller.smua.source.limitv = float(query["value"])
                return { }
            elif query["task"] == "set-smub-voltage-compliance":
                controller.smub.source.limitv = float(query["value"])
                return { }
            elif query["task"] == "set-smua-current":
                controller.apply_current(controller.smua, float(query["value"]))
                return { }
            elif query["task"] == "set-smub-current":
                controller.apply_current(controller.smub, float(query["value"]))
                return { }
            elif query["task"] == "set-smua-voltage":
                controller.apply_voltage(controller.smua, float(query["value"]))
                return { }
            elif query["task"] == "set-smub-voltage":
                controller.apply_voltage(controller.smub, float(query["value"]))
                return { }
            elif query["task"] == "measure-smua-current":
                return { "read": controller.smua.measure.i() }
            elif query["task"] == "measure-smub-current":
                return { "read": controller.smub.measure.i() }
            elif query["task"] == "measure-smua-voltage":
                return { "read": controller.smua.measure.v() }
            elif query["task"] == "measure-smub-voltage":
                return { "read": controller.smub.measure.v() }
        elif model == "LightField":
            if query["task"] == "activate":
                pi.try_activate_window()
                return { }
            elif query["task"] == "spectrum":
                pi.get_spectrum_direct()
                return { }
            elif query["task"] == "save-spectrum":
                pi.get_spectrum_autosave()
                return { "spectrum": [], "wavelengths": [] }

    def write(self, name, command):
        instrument = self.instruments[name]
        instrument.write(command)
        return { "wrote": command }

    def read(self, name):
        instrument = self.instruments[name]
        return { "read": instrument.read() }

    def query(self, name, command):
        instrument = self.instruments[name]
        return { "wrote": command, "read": instrument.query(command) }

    def stb(self, name):
        instrument = self.instruments[name]
        return { "name": name, "status": instrument.stb }

    def data_ready(self, name):
        status = self.stb(name)["status"]
        if status & STB_DATA_READY:
            return { "name": name, "dataReady": True }
        else:
            return { "name": name, "dataReady": False }

    def lock_instrument(self, name):
        instrument = self.instruments[name]
        key = instrument.lock()
        return { "name": name, "key": str(key) }

    def unlock_instrument(self, name):
        instrument = self.instruments[name]
        return { "name": name }

    def watch_lock(self, name):
        instrument = self.instruments[name]
        return { "name": name, "state": instrument.lock_state }

    def handle(self, query):
        logger.info("Query: %s", json.dumps(query))
        try:
            self.mutex_lock.acquire()
            command = query["function"]
            if command == "list":
                return json.dumps(self.list_resources())
            elif command == "open":
                return json.dumps(self.open_instrument(query["name"], query["address"]))
            elif command == "openModel":
                return json.dumps(self.open_model(query["name"], query["address"], query["model"]))
            elif command == "queryModel":
                return json.dumps(self.query_model(query["name"], query, query["model"]))
            elif command == "write":
                return json.dumps(self.write(query["name"], query["command"]))
            elif command == "read":
                return json.dumps(self.read(query["name"]))
            elif command == "query":
                return json.dumps(self.query(query["name"], query["command"]))
            elif command == "stb":
                return json.dumps(self.stb(query["name"]))
            elif command == "dataReady":
                return json.dumps(self.data_ready(query["name"]))
            elif command == "lock":
                return json.dumps(self.lock_instrument(query["name"]))
            elif command == "unlock":
                return json.dumps(self.unlock_instrument(query["name"]))
            elif command == "watchLock":
                return json.dumps(self.watch_lock(query["name"]))
            else:
                raise Exception('Invalid Command')
        except Exception as e:
            logger.error('%s\nFor query %s\n%s', repr(e), json.dumps(query), format_exc())
            return json.dumps({
                "error": repr(e),
                "errorType": str(type(e)),
                "errorTraceback": format_exc(),
                "query": json.dumps(query)
            })
        finally:
            self.mutex_lock.release()