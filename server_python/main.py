from http_server import HttpServer
import xml.etree.ElementTree as ET
import json

from mg.DataStorage import DataStorage
from mg.Factory import Factory
from mg.config import *


class RequestHandler:

    def __init__(self, server):
        self.response = None
        self.server = server

    def handle(self, payload):
        global MG_SERIALIZE_FORMAT
        global MG_XML

        request = Factory.create_command(payload)
        response = request.execute()

        sbuffer = ''
        if MG_SERIALIZE_FORMAT == MG_XML:
            root = ET.Element(response.get_type())
            response.serialize(root)
            sbuffer = ET.tostring(root)
        else:
            js = {response.get_type(): {}}
            response.serialize(js[response.get_type()])
            sbuffer = json.dumps(js)
        self.server.send(sbuffer)

if __name__ == '__main__':
    print 'run server:'
    DataStorage.shared().initialize(open('data.json').read())
    HttpServer.start(port=8045, request_handler_class=RequestHandler)
