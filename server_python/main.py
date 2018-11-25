from http_server import HttpServer

from mg.DataStorage import DataStorage
from mg.Factory import Factory
from mg.config import *


class RequestHandler:

    def __init__(self, server):
        self.response = None
        self.server = server

    def handle(self, payload):
        request = Factory.create_command(payload)
        response = request.execute()

        sbuffer = Factory.serialize_command(response)
        self.server.send(sbuffer)


if __name__ == '__main__':
    global MG_SERIALIZE_FORMAT
    global MG_XML

    data_file = 'data.xml' if MG_SERIALIZE_FORMAT == MG_XML else 'data.json'

    print 'run server:'
    DataStorage.shared().initialize(open(data_file).read())
    HttpServer.start(port=8045, request_handler_class=RequestHandler)
