from engine import *
import random


class Ball(Sprite):

    def __init__(self, engine, speed):
        Sprite.__init__(self, 'ball.png')
        self.engine = engine
        self.speed = speed

    def update(self, dt):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > self.engine.width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > self.engine.height:
            self.speed[1] = -self.speed[1]


if __name__ == '__main__':
    game = Engine()

    scene = Scene()
    ball = Ball(game, [10, 10])
    scene.add_child(ball)

    game.set_scene(scene)
    game.loop()
