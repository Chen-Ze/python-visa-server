import pyvisa
import json
import sys
import traceback
import threading

STB_DATA_READY = 1

class InstrumentController:
    def __init__(self):
        self.mutex_lock = threading.Lock()
        self.rm = pyvisa.ResourceManager()
        self.instruments = { }

    def list_resources(self):
        return self.rm.list_resources()

    def open_instrument(self, name, address):
        instrument = self.rm.open_resource(address)
        self.instruments[name] = instrument
        return { "instruments": str(self.instruments) }

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
        try:
            self.mutex_lock.acquire()
            command = query["function"]
            if command == "list":
                return json.dumps(self.list_resources())
            elif command == "open":
                return json.dumps(self.open_instrument(query["name"], query["address"]))
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
                return json.dumps({ "error": "Invalid Command." })
        except Exception as e:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            return json.dumps({ "error": str(ex_value), "errorType": str(ex_type), "errorTraceback": str(ex_traceback) })
        finally:
            self.mutex_lock.release()