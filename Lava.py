import pygame
from config import tile_size


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("images/lavaa.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


lava_group = pygame.sprite.Group()
