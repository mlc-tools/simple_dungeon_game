from http_server import HttpServer
import xml.etree.ElementTree as ET

from mg.DataStorage import DataStorage
from mg.Factory import Factory


class RequestHandler:

    def __init__(self, server):
        self.response = None
        self.server = server
        
    def handle(self, payload):
        request = Factory.create_command(payload)

        response = request.execute()

        root = ET.Element(response.get_type())
        response.serialize(root)
        sbuffer = ET.tostring(root)
        self.server.send(sbuffer)

if __name__ == '__main__':
    print 'run server:'
    DataStorage.shared().initialize(open('data.xml').read())
    HttpServer.start(port=8045, request_handler_class=RequestHandler)
