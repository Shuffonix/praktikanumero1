import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, variation):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/enemy_image.png")
        self.image.set_colorkey((255, 255, 255))
        self.origin = self.image.copy()
        self.size = 1
        self.variation = variation
        self.image = pygame.transform.smoothscale(self.origin, (self.size, self.size))
        self.center = (x + 25, y + 25)
        self.rect = self.image.get_bounding_rect()
        self.rect.center = self.center
        self.flag = False
        self.birth = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)
        self.worth = 2
        self.got_hit = False

    def update(self, dt, bullets):
        if self.got_hit:
            return self.worth
        now = pygame.time.get_ticks()
        if now - self.birth < 3000:
            self.worth = (now - self.birth)//100
            self.size += 15 * dt * self.variation
        elif now - self.birth < 5500:
            self.worth = (now - self.birth)//100
            self.size -= 15 * dt * self.variation
        else:
            self.kill()

        self.image = pygame.transform.smoothscale(self.origin, (abs(int(self.size)), abs(int(self.size))))
        self.rect = self.image.get_bounding_rect()
        self.rect.center = self.center
        self.mask = pygame.mask.from_surface(self.image)
