from urllib import request as urllib_request
import xml.etree.ElementTree as ET
import json
from mg.Factory import Factory
from mg.IVisitorResponse import IVisitorResponse
from mg import Config
from mg.common import *


class RequestManager:

    def __init__(self, controller, server_url):
        self.controller = controller
        self.server_url = server_url

    def request(self, request):
        payload = ''
        if Config.SUPPORT_XML_PROTOCOL:
            payload = serialize_command_to_xml(request)
        else:
            payload = serialize_command_to_json(request)
        print(payload)
        if isinstance(payload, bytes):
            payload = payload.decode()

        url = self.server_url.format(payload)
        url = url.replace('\n', '%20')
        url = url.replace(' ', '%20')
        print(url)

        response_message = urllib_request.urlopen(url).read()
        # Decode bytes to string for processing
        response_message = response_message.decode('utf-8').replace('\n', '')

        print(response_message)
        if Config.SUPPORT_XML_PROTOCOL:
            response = create_command_from_xml(response_message)
        else:
            response = create_command_from_json(response_message)
        response_handler = ResponseHandler(self.controller)
        response_handler.visit(response)


class ResponseHandler(IVisitorResponse):

    def __init__(self, controller):
        self.controller = controller
        IVisitorResponse.__init__(self)

    def visit_responseTileChangedState(self, ctx):
        self.controller.scene.tiles[ctx.index].data.state = ctx.state
        self.controller.scene.tiles[ctx.index].show_state()

    def visit_responseTileReward(self, ctx):
        self.controller.scene.gold += ctx.gold
        self.controller.scene.on_changed_gold()

        self.controller.scene.tiles[ctx.index].data.object = ctx.new_object
        self.controller.scene.tiles[ctx.index].show_state()
