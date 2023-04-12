import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.origin = pygame.image.load("circle-removebg-preview.png").convert_alpha()
        self.size = 1
        self.image = pygame.transform.scale(self.origin, (1153//(10*self.size), 655//(10*self.size)))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x + 25
        self.mask = pygame.mask.from_surface(self.image)
        self.counter = 0
        self.peak = False

    def update(self):
        if self.size < 10 and self.counter == 10 and not self.peak:
            self.counter = 0
            self.size += 1
        elif self.size > 0 and self.peak and self.counter == 10:
            self.size += 1
            self.counter = 0

        if self.peak < 10 and not self.peak:
            self.counter += 1
        else:
            self.counter -= 1


