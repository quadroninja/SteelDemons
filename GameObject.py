from utils import *
from pygame.math import Vector2

class GameObject:
    def __init__(self, pos, sprite, velocity, scale=(-1, -1)):
        self.pos = Vector2(pos)
        self.sprite = sprite
        self.size = Vector2(scale)
        if scale == (-1, -1):
            self.size = Vector2(self.sprite.get_size())
        self.sprite = pygame.transform.scale(self.sprite, self.size)
        self.width = self.size.x
        self.height = self.size.y
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        surface.blit(self.sprite, self.pos)

    def move(self, delta):
        self.pos += self.velocity * delta