import pygame


class Border(pygame.sprite.Sprite):

    def __init__(self, x, y, length, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotozoom(pygame.Surface((length, 10)), angle, 1)
        self.rect = self.image.get_bounding_rect()
        self.rect.x = x
        self.rect.y = y