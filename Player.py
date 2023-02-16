import pygame.sprite


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 75))
        self.rect = self.image.get_bounding_rect()
        self.rect.centery = 240
        self.rect.centerx = 320
