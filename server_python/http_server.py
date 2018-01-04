from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from urlparse import parse_qs

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
            self.send_header('content-type', 'text/html')
            self.end_headers()

            s = self.path
            args = parse_qs(s[2:])
            payload = args['request'][0]
            request_handler = HttpServer.request_handler_class(self)
            request_handler.handle(payload)

        except Exception as inst:
            self.wfile.write("error({})".format(inst.message))
            print "error({})".format(inst.message)
            
    def send(self, message):
        self.wfile.write(message)