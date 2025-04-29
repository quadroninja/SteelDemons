import pygame.time
from pygame.math import Vector2
from utils import *
from GameObject import GameObject


class Enemy(GameObject):
    def __init__(self, pos, spritesheet, speed, scale=(-1, -1), cols=1, rows=1, deathSound=None):
        super(Enemy, self).__init__(pos, spritesheet,
                                    Vector2(speed, 0), scale=scale)
        self.rect = pygame.Rect(0, 0, self.sprite.get_width() // cols,
                                self.sprite.get_height() // rows)
        self.cols = cols
        self.rows = rows
        self.deathSound = deathSound
        self.frame_cnt = round(1 / ENEMY_SPEED * 3) + 100
        self.frames = []
        self.current_frame = 0
        self.cut_frames()

    def cut_frames(self):
        for j in range(self.rows):
            for i in range(self.cols):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(self.sprite.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def draw(self, surface):
        self.frame_cnt += 1
        if self.frame_cnt > round(1 / ENEMY_SPEED * 3):
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.sprite = self.frames[self.current_frame]
            self.frame_cnt = 0
        surface.blit(self.sprite, self.pos)

    def collides_with(self, object):
        other_rect = object.sprite.get_rect(x=object.pos.x, y=object.pos.y)
        return self.sprite.get_rect(x=self.pos.x, y=self.pos.y).colliderect(other_rect)

    def death(self):
        self.deathSound.play()
