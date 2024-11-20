import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    # def __init__(self, tile_img, pos, groups):
    #     super().__init__(groups)
    #     self.image = tile_img
    #     self.rect = self.image.get_rect(topleft = pos)
    #     self.hitbox = self.rect.inflate(0, -5)
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, 0)
        if sprite_type == 'walls':
            self.hitbox = self.rect.inflate(0, -5)
        elif sprite_type == 'objects':
            pass