import pygame


# liikusin tagasi pygame Rect objekti peale, pildiga oli suuruse muutmine paras nuss
class Enemy():
    def __init__(self, screen, x, y):
        self.boss = False
        if self.boss:
            self.colour = (0, 0, 255)
        else:
            self.colour = (255, 0, 0)
        self.basesize = 24
        self.screen = screen

        self.x = x + 25
        self.y = y + 25

        self.circlerect = pygame.draw.circle(self.screen, self.colour, (self.x, self.y), 25-(self.basesize))
        self.flag = False
        self.counter = 0

    def update(self, speed=0):
        #print(self.circlerect)
        if self.counter == 20:

            if self.basesize > 23:
                self.flag = True
            elif self.basesize < 5:
                self.flag = False

            if self.flag:
                self.basesize -= 1 + speed
            else:
                self.basesize += 1 + speed
            self.counter = 0
        else:
            self.counter += 1

        self.circlerect = pygame.draw.circle(self.screen, (255, 0, 0), (self.x, self.y), 25-(self.basesize))

    def return_rect(self):
        return self.circlerect


