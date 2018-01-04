from engine import *
from client import RequestManager
from mg.DataStorage import DataStorage
from mg.TileState import TileState
from mg.RequestOpenTile import RequestOpenTile
from mg.RequestRewardFromTile import RequestRewardFromTile


class GameTile(Sprite):

    def __init__(self, data):
        Sprite.__init__(self, None)
        self.data = data
        self.object = None
        self.show_state()

    def create_object(self):
        if self.object:
            self.children.remove(self.object)

        self.object = Sprite(None)
        if self.data.object.name != 'empty':
            self.object.image_path = self.data.object.image
        self.add_child(self.object)
        self.object.pos = self.pos

    def show_state(self):
        self.image = None
        self.pos = self.data.x * 128, 128 + self.data.y * 128
        if self.data.state == TileState.closed:
            self.image_path = 'assets/tile_closed.png'
        else:
            self.image_path = 'assets/tile_open.png'
            self.create_object()


class Controller:

    def __init__(self, scene):
        self.scene = scene
        self.request_manager = RequestManager(self, 'http://localhost:8045/?request={}')

    def request_open_tile(self, tile):
        if tile.data.state == TileState.open:
            return
        request = RequestOpenTile()
        request.index = self.scene.data.get_tile_index(tile.data.x, tile.data.y)
        self.request_manager.request(request)

    def request_reward(self, tile):
        if not tile.data.object or not tile.data.object.interaction:
            return
        request = RequestRewardFromTile()
        request.index = self.scene.data.get_tile_index(tile.data.x, tile.data.y)
        self.request_manager.request(request)


class GameScene(Scene):

    def __init__(self):
        Scene.__init__(self)
        self.controller = Controller(self)
        self.data = DataStorage.shared().getDataLevel('0')
        self.gold = 0
        self.tiles = []
        self._init_level()

        self.gold_node = Text(font_size=100)
        self.add_child(self.gold_node)
        self.on_changed_gold()

    def _init_level(self):
        for tile in self.data.tiles:
            sprite = GameTile(tile)
            self.add_child(sprite)
            self.tiles.append(sprite)

    def mouse_click(self, pos):
        tile = None
        for s in self.tiles:
            if s.rect.move(s.pos).collidepoint(pos):
                tile = s
        if tile:
            if tile.data.state == TileState.closed:
                self.controller.request_open_tile(tile)
            else:
                self.controller.request_reward(tile)

    def on_changed_gold(self):
        self.gold_node.set_text(str(self.gold))
        rect = self.gold_node.renderer.get_rect()
        self.gold_node.pos = [320 - rect.width / 2, 30]


if __name__ == '__main__':
    game = Engine()
    DataStorage.shared().initialize(open('assets/data.xml').read())

    scene = GameScene()

    game.set_scene(scene)
    game.loop()
