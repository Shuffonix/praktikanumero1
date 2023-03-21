import pygame
from Gun import Gun
pygame.init()

screen = pygame.display.set_mode((640, 480))

running = True
clock = pygame.time.Clock()
gun = Gun(320, 240)
gun_group = pygame.sprite.Group()
gun_group.add(gun)

while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    gun_group.update(mouse_x, mouse_y)
    screen.fill((0, 0, 0))
    gun_group.draw(screen)
    pygame.display.flip()
pygame.quit()
