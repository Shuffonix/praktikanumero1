import pygame


class Gun(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 15), pygame.SRCALPHA)
        self.image.fill((100, 100, 100))
        self.origin = self.image.copy()
        self.rect = self.image.get_bounding_rect()
        self.center = (x, y)
        self.rect.centerx = x
        self.rect.centery = y
        self.last_shot = pygame.time.get_ticks()
        self.cd_overlay = self.image.copy()
        self.cd_rect = self.cd_overlay.get_bounding_rect()
        self.protsent = 100
        self.mask = pygame.mask.from_surface(self.image)
        self.last_value = None
        self.hit = False

    def update(self, x, y, degs, screen):
        now = pygame.time.get_ticks()
        self.protsent = min(int((now - self.last_shot)/5), 100)
        cooldown = int(min(0.49 * self.protsent, 49)) + 1
        cd_overlay = pygame.Surface((cooldown, 15), pygame.SRCALPHA)

        # värvimise loogika(ish)
        if self.hit:
            cd_overlay.fill((255, 0, 0))
        else:
            cd_overlay.fill((255, 255, 255))

        self.cd_overlay = pygame.transform.rotozoom(cd_overlay, degs, 1)
        self.image = pygame.transform.rotozoom(self.origin, degs, 1)
        self.rect = self.image.get_rect(center=self.center)
        self.cd_rect = self.cd_overlay.get_rect()
        if 0 > degs:
            self.cd_rect.top = self.rect.top
        else:
            self.cd_rect.bottom = self.rect.bottom

        if abs(degs) > 90:
            self.cd_rect.right = self.rect.right
        else:
            self.cd_rect.left = self.rect.left
        self.mask = pygame.mask.from_surface(self.image)
