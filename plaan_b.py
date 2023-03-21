import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))

running = True
clock = pygame.time.Clock()


while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
