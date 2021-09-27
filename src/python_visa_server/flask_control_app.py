from flask import Flask
from flask import request

import python_visa_server.instrument_control as instrument_control

instrument_controller = instrument_control.InstrumentController()

app = Flask(__name__)

@app.route('/controller')
def controller():
    return instrument_controller.handle(request.args)

if __name__ == "__main__":
    app.run(debug=True)