import pygame


class Border(pygame.sprite.Sprite):

    def __init__(self, x, y, length, horizontal):
        pygame.sprite.Sprite.__init__(self)
        self.start = (x, y)
        if horizontal:
            self.end = (x+length, y)
        else:
            self.end = (x, y+length)

        """if horizontal:
            self.object = pygame.Rect(x, y, length, 1)
        else:
            self.object = pygame.Rect(x, y, 1, length)"""

    def draw(self, screen):
        pygame.draw.line(screen, (0, 0, 0), self.start, self.end, 5)
