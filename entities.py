import pygame
from sprite import *
from utils import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = Spritesheet(getImagePath("samurai.png"))
        self.idle = [pygame.transform.scale(self.sprite.get_sprite(0, 64, 128, 64), (140,140)), pygame.transform.scale(self.sprite.get_sprite(128, 0, 128, 64), (140,140))]
        self.sword = [pygame.transform.scale(self.sprite.get_sprite(128, 64, 128, 64), (140,140)),
                      pygame.transform.scale(self.sprite.get_sprite(256, 64, 128, 64), (140,140)),
                      pygame.transform.scale(self.sprite.get_sprite(384, 64, 128, 64), (140,140)),
                      pygame.transform.scale(self.sprite.get_sprite(0, 0, 128, 64), (140,140))
                      ]
        self.state = 0
        self.animation = 'idle'
        self.image = self.idle[0]
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.state += 0.15
        if self.state >= len(self.sword):
            self.state = 0
        self.image = self.sword[int(self.state)]
