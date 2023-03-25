import pygame
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = random.randint(30, 90)
        self.image = pygame.Surface((50, self.width), pygame.SRCALPHA)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_bounding_rect()
        self.rect.y = y
        self.rect.x = x
        self.mask = pygame.mask.from_surface(self.image)
        # self.horizontal =
