import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_bounding_rect()
        self.rect.y = y
        self.rect.x = x
        self.mask = pygame.mask.from_surface(self.image)
