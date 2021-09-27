from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, parse_qsl
import logging
import coloredlogs

import deprecation

import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
src_dir = os.path.join(file_dir, "src")
sys.path.append(src_dir)

import src.python_visa_server.instrument_control as instrument_control

instrument_controller = instrument_control.InstrumentController()

coloredlogs.install()
logging.warning("Module http_control is deprecated.")

class InstrumentHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        request = urlparse(self.path)
        if request.path == "/controller":
            parsed_query = dict(parse_qsl(request.query))
            print(parsed_query)
            self.wfile.write(instrument_controller.handle(parsed_query).encode('utf-8'))
        else:
            self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

@deprecation.deprecated()
def run(server_class=HTTPServer, handler_class=InstrumentHandler, port=8888):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()