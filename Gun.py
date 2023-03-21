import pygame


class Gun(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 10), pygame.SRCALPHA)
        self.image.fill((0, 0, 0))
        self.origin = self.image.copy()
        self.rect = self.image.get_bounding_rect()
        self.center = (x, y)
        self.rect.centerx = x
        self.rect.centery = y

    def update(self, x, y, degs):
        self.image = self.origin.copy()
        self.image = pygame.transform.rotozoom(self.image, degs, 1)
        self.rect = self.image.get_rect(center=self.center)
