import urllib2
import xml.etree.ElementTree as ET
import json
from mg.Factory import Factory
from mg.IVisitorResponse import IVisitorResponse
from mg import Config


class RequestManager:

    def __init__(self, controller, server_url):
        self.controller = controller
        self.server_url = server_url

    def request(self, request):
        payload = ''
        if Config.SUPPORT_XML_PROTOCOL:
            root = ET.Element(request.get_type())
            request.serialize_xml(root)
            payload = ET.tostring(root)
        else:
            dict_ = {}
            request.serialize_json(dict_)
            dict_ = {request.get_type(): dict_}
            payload = json.dumps(dict_)
        print payload

        url = self.server_url.format(payload)
        url = url.replace('\n', '%20')
        url = url.replace(' ', '%20')

        response_message = urllib2.urlopen(url).read()
        response_message = response_message.replace('\n', '')

        print response_message
        if Config.SUPPORT_XML_PROTOCOL:
            response = Factory.create_command_from_xml(response_message)
        else:
            response = Factory.create_command_from_json(response_message)
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
