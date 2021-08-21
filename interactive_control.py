import instrument_control
import json

instrument_controller = instrument_control.InstrumentController()

if __name__ == "__main__":
    while True:
        command_raw = input(">>> ")
        if command_raw == "quit":
            break
        try:
            command = json.loads(command_raw)
            result = instrument_controller.handle(command)
            print(result)
        except Exception as e:
            print(e)
            continue

