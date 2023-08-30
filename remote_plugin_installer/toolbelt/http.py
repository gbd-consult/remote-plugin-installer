from http.server import BaseHTTPRequestHandler, HTTPServer

from qgis.PyQt.QtCore import QThread, pyqtSignal


class AddressInUseException(Exception):
    pass


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args):
        BaseHTTPRequestHandler.__init__(self, *args)

    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        content_length = int(
            self.headers["Content-Length"]
        )  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        with open(self.server.filename, "wb") as tempfile:
            tempfile.seek(0)
            tempfile.write(post_data)
        self.server.has_file = True

        self._set_response()
        self.wfile.write("file received".encode("utf-8"))


class MyHTTPServer(HTTPServer):
    def __init__(self, filename, *args):
        HTTPServer.__init__(self, *args)
        self.filename = filename


class ServerThread(QThread):
    output = pyqtSignal()

    def __init__(self, filename, parent=None, port=6789):
        QThread.__init__(self, parent)
        self.exiting = False
        self.tempfile = filename
        try:
            self.httpd = MyHTTPServer(filename, ("", port), RequestHandler)
        except OSError:
            raise AddressInUseException

    def run(self):
        while not self.exiting:
            self.httpd.handle_request()
            self.output.emit()
