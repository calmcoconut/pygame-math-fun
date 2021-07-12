import pygame


class Spritesheet(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))  # default black when PNG
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite
