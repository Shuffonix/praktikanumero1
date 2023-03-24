import random
import pygame
from random import randint
from math import atan2, degrees, cos, sin, radians
from particle import Particle


# sry ma ei saa sellest Group asjast ikka veel aru, seega ma ei kasuta toda lol
class Bullet():
    def __init__(self, x, y, rad):
        self.bounces = 0
        self.velocity = 100
        self.rad = rad
        self.dx = cos(self.rad) * self.velocity
        self.dy = -sin(self.rad) * self.velocity  # fuck põdra ja fuck matemaatika bruh
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    # uuendab neid maagilisi asju siin, sest siin on seda kõige mugavam teha lol


    def update_angle(self):
        self.dx = cos(self.rad) * self.velocity
        self.dy = -sin(self.rad) * self.velocity

    def update(self, dt):
        self.rect.x += self.dx * dt
        self.rect.y += self.dy * dt

        #self.rect = pygame.Rect((self.x, self.y, 10, 10))

    # pmst tagastab mitu particle-it see kuul omab
    def explode(self):
        number = randint(8, 24)
        particles = [Particle(self.x, self.y) for i in range(number)]
        return particles

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
