from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlsplit, parse_qs


class HttpServer(BaseHTTPRequestHandler):
    request_handler_class = None

    @staticmethod
    def start(port, request_handler_class):
        HttpServer.request_handler_class = request_handler_class
        server = HTTPServer(("localhost", port), HttpServer)
        server.serve_forever()

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # Parse query string safely
            parsed = urlsplit(self.path)
            args = parse_qs(parsed.query)
            payload = args.get('request', [''])[0]
            if isinstance(payload, bytes):
                payload = payload.decode()
            request_handler = HttpServer.request_handler_class(self)
            request_handler.handle(payload)

        except Exception as inst:
            msg = "error({})".format(str(inst))
            self.wfile.write(msg.encode('utf-8'))
            print(msg)

    def send(self, message):
        if isinstance(message, bytes):
            self.wfile.write(message)
        else:
            self.wfile.write(str(message).encode('utf-8'))
