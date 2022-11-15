from http.server import BaseHTTPRequestHandler, HTTPServer
from tempfile import NamedTemporaryFile

from post_plugin.toolbelt.plugin_install import install


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        content_length = int(
            self.headers["Content-Length"]
        )  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        with NamedTemporaryFile() as file:
            file.write(post_data)
            install(file.name)
            print(file.name)

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode("utf-8"))


def run_server(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    return httpd
