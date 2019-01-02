from http_server import HttpServer

from mg.DataStorage import DataStorage
from mg.Factory import Factory
from mg import Config


class RequestHandler:

    def __init__(self, server):
        self.response = None
        self.server = server

    def handle(self, payload):
        if Config.SUPPORT_XML_PROTOCOL:
            request = Factory.create_command_from_xml(payload)
        else:
            request = Factory.create_command_from_json(payload)
        response = request.execute()

        if Config.SUPPORT_XML_PROTOCOL:
            body = Factory.serialize_command_to_xml(response)
        else:
            body = Factory.serialize_command_to_json(response)
        self.server.send(body)


if __name__ == '__main__':
    if Config.SUPPORT_XML_PROTOCOL:
        DataStorage.shared().initialize_xml(open('data.xml').read())
    else:
        DataStorage.shared().initialize_json(open('data.json').read())

    print 'run server:'
    HttpServer.start(port=8045, request_handler_class=RequestHandler)
