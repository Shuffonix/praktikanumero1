import pygame


class Explosion(pygame.sprite.Sprite):

    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.anims = []
        for i in range(9):
            img = pygame.image.load("assets/explosion_anim/regularExplosion0" + str(i) + ".png").convert()
            img.set_colorkey((0, 0, 0))
            img = pygame.transform.scale(img, (self.size, self.size))
            self.anims.append(img)
        self.image = self.anims[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.anims):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.anims[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
