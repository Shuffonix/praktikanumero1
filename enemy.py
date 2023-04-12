import pygame


# liikusin tagasi pygame Rect objekti peale, pildiga oli suuruse muutmine paras nuss
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemy_image.png")
        self.image.set_colorkey((255, 255, 255))
        self.origin = self.image.copy()
        self.size = 1
        self.image = pygame.transform.smoothscale(self.origin, (self.size, self.size))
        self.center = (x, y)
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
            self.size += 10 * dt
        elif now - self.birth < 5500:
            self.worth = 1
            self.size -= 10 * dt
        else:
            self.kill()
        self.image = pygame.transform.smoothscale(self.origin, (int(self.size), int(self.size)))
        print(self.image.get_size())
        self.rect = self.image.get_bounding_rect()
        self.rect.center = self.center
        """if self.counter == 20:
            if self.basesize > 23:
                self.flag = True
            elif self.basesize < 5:
                self.flag = False

            if self.flag:
                self.basesize -= 1
            else:
                self.basesize += 1
            self.counter = 0
        else:
            self.counter += 1"""

