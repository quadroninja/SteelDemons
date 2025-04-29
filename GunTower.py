from utils import *
from GameObject import GameObject
from Bullet import Bullet
import math
from pygame.math import Vector2


class GunTower(GameObject):
    def __init__(self, pos, sprite, pivot, reload, bullet_callback, scale=(-1, -1)):
        super().__init__(pos, sprite, 0, scale=scale)
        self.angle = 0
        self.shooting_sound = load_sound('shoot')
        self.shooting_sound.set_volume(0.6)
        self.pivot = Vector2(round(self.size[0] * pivot[0]), round(self.size[1] * pivot[1]))
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.angle = 0
        self.image = None
        self.rotate()
        self.cooldown = 0
        self.reloadTime = reload
        self.create_bullet_callback = bullet_callback
        self.overheated = False

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = int(math.degrees(-math.atan2(mouse_y - self.pos.y, mouse_x - self.pos.x))) - 90
        w, h = self.size
        img2 = pygame.Surface((w * 2, h * 2), pygame.SRCALPHA)
        img2.blit(self.sprite, (w - self.pivot[0], h - self.pivot[1]))
        self.image = pygame.transform.rotate(img2, self.angle)

    def draw(self, surface):
        if self.image is not None:
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            surface.blit(self.image, self.rect)

    def shoot(self):
        if self.cooldown >= self.reloadTime and not self.overheated:
            self.shooting_sound.play()
            bullet = Bullet(Vector2(self.pos.x - math.cos(math.radians(-self.angle + 90)) * self.pivot.y,
                                    self.pos.y - math.sin(math.radians(-self.angle + 90)) * self.pivot.y),
                            load_sprite('bullet.png'),
                            Vector2(-math.cos(math.radians(-self.angle + 90)) * BULLET_VELOCITY,
                                    -math.sin(math.radians(-self.angle + 90)) * BULLET_VELOCITY),
                            scale=Vector2(10, 30))
            self.create_bullet_callback(bullet)
            self.cooldown = 0
