from utils import *
from GameObject import GameObject
from pygame.math import Vector2
import math

class Bullet(GameObject):
    def __init__(self, pos, sprite, velocity, scale=Vector2(-1, -1)):

        super().__init__(pos, sprite, velocity)
        angleCalcVector = Vector2(0, -1)
        scalar = velocity.x * angleCalcVector.x + velocity.y * angleCalcVector.y
        modulea = math.sqrt(velocity.x * velocity.x + velocity.y * velocity.y)
        moduleb = math.sqrt(angleCalcVector.x * angleCalcVector.x + angleCalcVector.y * angleCalcVector.y)
        size = scale
        if size.xy == (-1, -1):
            size = Vector2(self.sprite.get_size())
        self.sprite = pygame.transform.scale(self.sprite, size)
        self.sprite = pygame.transform.rotate(self.sprite, math.degrees(math.acos(scalar / moduleb / modulea)))