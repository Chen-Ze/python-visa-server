from waitress import serve
import argparse
import logging
import coloredlogs

import python_visa_server.flask_control_app as flask_control_app

parser = argparse.ArgumentParser(description='Serve the flask app for instrument control.')
parser.add_argument('--port', metavar='port', type=int, help='port for the', default=8888)

args = parser.parse_args()
port = args.port

coloredlogs.install()

logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)

serve(flask_control_app.app, host='0.0.0.0', port=port)