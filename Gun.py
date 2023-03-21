import pygame
from math import atan2, degrees, pi


class Gun(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 20))
        self.image.fill((255, 255, 255))
        self.origin = self.image.copy()
        self.rect = self.image.get_rect()
        self.center = (x, y)
        self.rect.centerx = x
        self.rect.centery = y
    def update(self, x, y):
        self.image = self.origin.copy()
        dx = x - self.rect.centerx
        dy = y - self.rect.centery
        rads = atan2(-dy, dx)
        rads %= 2*pi
        degs = degrees(rads)
        self.image = pygame.transform.rotozoom(self.image, degs, 1)
        self.rect = self.image.get_rect(center=self.center)
