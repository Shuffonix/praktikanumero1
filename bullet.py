import pygame
from math import degrees, cos, sin, atan2, pi


class Bullet(pygame.sprite.Sprite):
    def __init__(self, rad):
        pygame.sprite.Sprite.__init__(self)
        self.bounces = 0
        self.velocity = 1000
        self.rad = rad
        self.dx = cos(self.rad)
        self.dy = -sin(self.rad)  # fuck põdra ja fuck matemaatika bruh
        self.origin = pygame.image.load("bullet_image.png")
        self.image = pygame.transform.rotozoom(self.origin, degrees(self.rad), 1)
        self.rect = self.image.get_rect()
        self.x = 320
        self.y = 240
        self.mask = pygame.mask.from_surface(self.image)
        self.collisions = 0
        self.last_porge = None

    # uuendab neid maagilisi asju siin, sest siin on seda kõige mugavam teha lol
    def collision(self, borders):
        collisions = 0
        for border in borders:
            if pygame.sprite.collide_mask(self, border):
                if border == self.last_porge:
                    continue
                collisions = 1

                if border.angle == 90:
                    self.dx *= -1
                else:
                    self.dy *= -1
                self.last_porge = border
                self.rad = atan2(self.dy, -self.dx)
                self.velocity *= 0.75
                self.image = pygame.transform.rotozoom(self.origin, degrees(pi + self.rad), 1)
                self.mask = pygame.mask.from_surface(self.image)
        self.collisions += collisions

    def update(self, dt, borders):
        self.x += self.dx * dt * self.velocity
        self.y += self.dy * dt * self.velocity

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        self.collision(borders)
        if self.collisions > 3:
            self.kill()
