from os.path import isfile, join
from http.server import BaseHTTPRequestHandler, HTTPServer


SERVER_ADDR = "10.0.0.74"
SERVER_PORT = 80

SERVER_DIR = "http"

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        file_path = join(SERVER_DIR, self.path.split("/")[-1])
        if file_path == SERVER_DIR + "/":  # / for linux \\ for windows
            print("Sending index page")
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Cache-Control', 'max-age=0, no-cache, no-store')
            self.send_header('Pragma', 'no-cache')
            self.send_header('X-Organization', 'Nintendo')
            self.end_headers()
            self.wfile.write(open(file_path + "index.html", "rb").read())
        else:
            print("Sending 404 for {}".format(file_path))
            self.send_response(404)
            self.end_headers()


def run():
    with HTTPServer((SERVER_ADDR, SERVER_PORT), HTTPHandler) as httpd:
        print("Serving on port {}".format(SERVER_PORT))
        httpd.serve_forever()