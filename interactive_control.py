import json
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
src_dir = os.path.join(file_dir, "src")
sys.path.append(src_dir)

import src.python_visa_server.instrument_control as instrument_control

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

