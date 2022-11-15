from http.server import BaseHTTPRequestHandler, HTTPServer


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
        print(post_data)

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode("utf-8"))


def run_server(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    return httpd
