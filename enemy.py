import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.origin = pygame.image.load("circle-removebg-preview.png").convert_alpha()

        self.image = pygame.transform.scale(self.origin, (1153//10, 655//10))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x + 25
        self.mask = pygame.mask.from_surface(self.image)
