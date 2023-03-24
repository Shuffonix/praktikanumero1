import pygame
from math import degrees, cos, sin


# sry ma ei saa sellest Group asjast ikka veel aru, seega ma ei kasuta toda lol
class Bullet(pygame.sprite.Sprite):
    def __init__(self, rad):
        pygame.sprite.Sprite.__init__(self)
        self.bounces = 0
        self.velocity = 1000
        self.rad = rad
        self.dx = cos(self.rad)
        self.dy = -sin(self.rad)  # fuck põdra ja fuck matemaatika bruh
        self.origin = pygame.Surface((20, 10), pygame.SRCALPHA)
        self.origin.fill((255, 110, 0))
        self.image = pygame.transform.rotozoom(self.origin, degrees(rad), 1)
        self.rect = self.image.get_rect()
        self.x = 320
        self.y = 240

    # uuendab neid maagilisi asju siin, sest siin on seda kõige mugavam teha lol

    def update(self, dt):
        self.x += self.dx * dt * self.velocity
        self.y += self.dy * dt * self.velocity

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    # pmst tagastab mitu particle-it see kuul omab

