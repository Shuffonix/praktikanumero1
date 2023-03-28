import pygame


class Border(pygame.sprite.Sprite):

    def __init__(self, x, y, length, angle):
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle
        self.image = pygame.Surface((length, 10), pygame.SRCALPHA)
        self.image.fill((255, 255, 255))
        self.image = pygame.transform.rotozoom(self.image, angle, 1)
        self.rect = self.image.get_bounding_rect()
        self.rect.y = y
        self.rect.x = x
        self.mask = pygame.mask.from_surface(self.image)
