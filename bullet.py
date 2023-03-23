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
        self.velocity = 10
        self.rad = rad
        self.dx = cos(self.rad) * self.velocity
        self.dy = -sin(self.rad) * self.velocity  # fuck põdra ja fuck matemaatika bruh
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_bounding_rect()
        self.rect.centerx = 320
        self.rect.centery = 240

    # uuendab neid maagilisi asju siin, sest siin on seda kõige mugavam teha lol

    def update(self, dt):
        self.rect.x += self.dx * dt
        self.rect.y += self.dy * dt
        print(self.rect.center)

    # pmst tagastab mitu particle-it see kuul omab
    def explode(self):
        number = randint(8, 24)
        particles = [Particle(self.rect.x, self.rect.y) for i in range(number)]
        return particles
