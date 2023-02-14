import pygame.sprite


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, pilt=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((41, 41))
        self.image.fill((150, 255, 150))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.id = (x, y)
        self.sides = [False, False, False, False]

    def update(self, global_x, global_y, block_dict):
        self.rect.x = self.x - global_x
        self.rect.y = self.y - global_y

        # ülemine naaber
        if (self.x, self.y - 40) in block_dict:
            self.sides[0] = True
        else:
            pygame.draw.line(self.image, (0, 0, 0), (0, 0), (40, 0), 5)
            self.sides[0] = False

        # parem naaber
        if (self.x + 40, self.y) in block_dict:
            self.sides[1] = True
        else:
            pygame.draw.line(self.image, (0, 0, 0), (40, 0), (40, 40), 5)
            self.sides[1] = False

        # alumine naaber
        if (self.x, self.y + 40) in block_dict:
            self.sides[2] = True
        else:
            pygame.draw.line(self.image, (0, 0, 0), (40, 40), (0, 40), 5)
            self.sides[2] = False

        # vasak naaber
        if (self.x - 40, self.y) in block_dict:
            self.sides[3] = True
        else:
            pygame.draw.line(self.image, (0, 0, 0), (0, 40), (0, 0), 5)
            self.sides[3] = False
