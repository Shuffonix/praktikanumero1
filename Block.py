import pygame.sprite


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, pilt=None):
        pygame.sprite.Sprite.__init__(self)
        self.origin = pygame.Surface((40, 40))
        self.origin.fill((150, 255, 150))
        self.image = self.origin.copy()
        self.rect = self.origin.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x + 1
        self.rect.y = y + 1
        self.id = (x, y)
        self.sides = [True, True, True, True]

    def update(self, global_x, global_y, block_dict, check_neighbors=False):
        self.image = self.origin.copy()
        self.rect.x = self.x - global_x + 1
        self.rect.y = self.y - global_y + 1

        if check_neighbors:
            # ülemine naaber
            if (self.x, self.y - 40) in block_dict:
                self.sides[0] = True
            else:
                self.sides[0] = False

            # parem naaber
            if (self.x + 40, self.y) in block_dict:
                self.sides[1] = True
            else:
                self.sides[1] = False

            # alumine naaber
            if (self.x, self.y + 40) in block_dict:
                self.sides[2] = True
            else:

                self.sides[2] = False

            # vasak naaber
            if (self.x - 40, self.y) in block_dict:
                self.sides[3] = True
            else:
                self.sides[3] = False

        if not self.sides[0]:
            pygame.draw.line(self.image, (0, 0, 0), (0, 0), (39, 0), 5)
        if not self.sides[1]:
            pygame.draw.line(self.image, (0, 0, 0), (39, 0), (39, 40), 5)
        if not self.sides[2]:
            pygame.draw.line(self.image, (0, 0, 0), (39, 39), (0, 39), 5)
        if not self.sides[3]:
            pygame.draw.line(self.image, (0, 0, 0), (0, 39), (0, 0), 5)
