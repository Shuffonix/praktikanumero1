import random
import pygame
from random import randint
from math import atan2, degrees, cos, sin, radians
from particle import Particle


# sry ma ei saa sellest Group asjast ikka veel aru, seega ma ei kasuta toda lol
class Bullet(pygame.sprite.Sprite):
    def __init__(self, rad):
        pygame.sprite.Sprite.__init__(self)
        self.bounces = 0
        self.velocity = 0.0001
        self.rad = rad
        self.dx = cos(self.rad)
        self.dy = -sin(self.rad)  # fuck põdra ja fuck matemaatika bruh
        self.image = pygame.transform.rotozoom(pygame.Surface((10, 10)), degrees(rad), 1)
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_bounding_rect()
        self.rect.centerx = 320
        self.rect.centery = 240

    # uuendab neid maagilisi asju siin, sest siin on seda kõige mugavam teha lol

    def update(self, dt):
        print(self.dy)
        self.rect.x += self.dx * dt
        self.rect.y += self.dy * dt

    # pmst tagastab mitu particle-it see kuul omab

