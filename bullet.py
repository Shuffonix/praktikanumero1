import pygame
from math import degrees, cos, sin, atan2


class Bullet(pygame.sprite.Sprite):
    def __init__(self, rad):
        pygame.sprite.Sprite.__init__(self)
        self.bounces = 0
        self.velocity = 1000
        self.rad = rad
<<<<<<< HEAD
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
=======
        self.dx = cos(self.rad)
        self.dy = -sin(self.rad)  # fuck põdra ja fuck matemaatika bruh
        self.origin = pygame.Surface((20, 10), pygame.SRCALPHA)
        self.origin.fill((255, 100, 0))
        self.image = pygame.transform.rotozoom(self.origin, degrees(self.rad), 1)
        self.rect = self.image.get_rect()
        self.x = 320
        self.y = 240
        self.mask = pygame.mask.from_surface(self.image)
        self.collisions = 0

    # uuendab neid maagilisi asju siin, sest siin on seda kõige mugavam teha lol
    def collision(self, borders):
        collisions = 0
        for border in borders:
            if pygame.sprite.collide_mask(self, border):
                collisions = 1

                if border.angle == 90:
                    self.dx *= -1
                else:
                    self.dy *= -1
>>>>>>> trevori-branch

                self.rad = atan2(self.dy, -self.dx)
                self.image = pygame.transform.rotozoom(self.origin, degrees(self.rad), 1)
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
