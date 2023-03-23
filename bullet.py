import pygame
from random import randint
from math import atan2, degrees, cos, sin, radians

# sry ma ei saa sellest Group asjast ikka veel aru, seega ma ei kasuta toda lol
class Bullet():
    def __init__(self, x, y, rad):

        self.velocity = 100
        self.dx = cos(rad) * self.velocity
        self.dy = -sin(rad) * self.velocity  # fuck põdra ja fuck matemaatika bruh
        self.x = x
        self.y = y
        self.image = pygame.Rect((self.x, self.y, 10, 10))
        self.rad = rad

    def update(self, dt):
        self.x = self.x + self.dx * dt
        self.y = self.y + self.dy * dt
        self.image = pygame.Rect((self.x, self.y, 10, 10))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.image)
