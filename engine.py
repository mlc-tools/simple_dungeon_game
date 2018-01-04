import sys
import pygame


class Engine:

    def __init__(self, show_fps=True, fps=60):
        pygame.init()
        self.width, self.height = 800, 640
        self.win_size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.win_size)
        self.show_fps = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.scene = None
        self.next_scene = None

    def set_scene(self, scene):
        self.next_scene = scene

    def loop(self):

        font = pygame.font.Font(None, 30)

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if self.scene is not None:
                self.scene.draw(self.screen)

            if self.show_fps:
                fps = font.render(str(int(self.clock.get_fps())), True, pygame.Color('white'))
                self.screen.blit(fps, (0, 0))

            pygame.display.flip()
            ms = self.clock.tick(self.fps)
            if self.next_scene is not None:
                print 'switch_scene'
                self.scene = self.next_scene
                self.next_scene = None
            if self.scene is not None:
                self.scene.update(ms / 1000.0)


class Node:

    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.children = []

    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def draw(self, screen):
        for child in self.children:
            child.draw(screen)

    def add_child(self, node):
        self.children.append(node)


class Scene(Node):

    def __init__(self):
        Node.__init__(self)

    def draw(self, screen):
        screen.fill((100, 0, 0))
        Node.draw(self, screen)


class Sprite(Node):

    def __init__(self, image):
        Node.__init__(self)
        self.image_path = image
        self.image = None

    def draw(self, screen):
        if self.image is None and self.image_path is not None:
            self._load_image()
        if self.image:
            screen.blit(self.image, self.rect)

    def _load_image(self):
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
