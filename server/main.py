from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from urlparse import parse_qs
import xml.etree.ElementTree as ET

from mg.Factory import Factory
from mg.IVisitorRequest import IVisitorRequest
from mg.DataStorage import DataStorage
from mg.ResponseTileReward import ResponseTileReward
from mg.ResponseTileChangedState import ResponseTileChangedState
from mg.TileState import TileState


class RequestHandler(IVisitorRequest):

    def __init__(self):
        IVisitorRequest.__init__(self)
        self.response = None

    def visit_requestOpenTile(self, ctx):
        # tile.data.state = TileState.open
        self.response = ResponseTileChangedState()
        self.response.index = ctx.index
        self.response.state = TileState.open

    def visit_requestRewardFromTile(self, ctx):
        data = DataStorage.shared().getDataLevel('0')
        tile = data.tiles[ctx.index]
        self.response = ResponseTileReward()
        self.response.index = ctx.index
        self.response.gold = tile.object.reward_gold
        self.response.new_object = tile.object.next


class HttpServer(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            s = self.path
            args = parse_qs(s[2:])
            payload = args['request'][0]
            request = Factory.create_command(payload)

            requestHandler = RequestHandler()
            requestHandler.visit(request)

            if requestHandler.response:
                root = ET.Element(requestHandler.response.get_type())
                requestHandler.response.serialize(root)
                sbuffer = ET.tostring(root)
                self.wfile.write(sbuffer)

        except Exception as inst:
            self.wfile.write("error({})".format(inst.message))
            print "error({})".format(inst.message)
            exit(0)


if __name__ == '__main__':
    port = 8045
    DataStorage.shared().initialize(open('data.xml').read())

    print 'run server:'
    server = HTTPServer(("localhost", port), HttpServer)
    server.serve_forever()
