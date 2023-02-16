import pygame.sprite


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, pilt=None):
        pygame.sprite.Sprite.__init__(self)

        # ˅˅˅ ajutine, kuni lisame pildid blockidele
        self.origin = pygame.Surface((40, 40))
        self.origin.fill((150, 255, 150))
        # ˄˄˄

        self.image = self.origin.copy()
        self.rect = self.origin.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x + 1
        self.rect.y = y + 1
        self.id = (x, y)
        self.sides = [True, True, True, True]

    def update(self, global_x, global_y, block_dict, visible_blocks, check_neighbors=False):
        self.rect.x = self.x - global_x + 1
        self.rect.y = self.y - global_y + 1
        if self.rect.right > 0 and self.rect.left < 640 and self.rect.bottom > 0 and self.rect.top < 480:
            visible_blocks.add(self)
        else:
            visible_blocks.remove(self)
        if check_neighbors:
            # uus puhta pildi koopia
            self.image = self.origin.copy()

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
