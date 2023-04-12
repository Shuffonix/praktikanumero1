import pygame
from math import degrees, cos, sin, atan2, pi, radians
from random import randint


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
        self.dead = False

    # uuendab neid maagilisi asju siin, sest siin on seda kõige mugavam teha lol
    def collision(self, borders):
        particles = []
        for border in borders:
            if pygame.sprite.collide_mask(self, border):
                if border == self.last_porge:
                    continue
                self.collisions += 1

                if border.angle % 180 == 0:
                    self.dy *= -1
                else:
                    self.dx *= -1

                if self.collisions < 4:
                    death_particle = 0
                    amount = 3
                else:
                    death_particle = 1
                    amount = 1

                for i in range(amount):
                    particles.append([
                        0.2,
                        radians(randint(border.angle - 110, border.angle - 70)),
                        list(self.rect.center),
                        death_particle
                    ])

                self.last_porge = border
                self.rad = atan2(self.dy, -self.dx)
                self.velocity *= 0.75
                self.image = pygame.transform.rotozoom(self.origin, degrees(pi + self.rad), 1)
                self.mask = pygame.mask.from_surface(self.image)
        return particles

    def update(self, dt, borders, screen):
        if self.dead:
            self.kill()

        self.x += self.dx * dt * self.velocity
        self.y += self.dy * dt * self.velocity

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        particle_list = self.collision(borders)

        if self.collisions > 3:
            self.dead = True

        if particle_list:
            return particle_list