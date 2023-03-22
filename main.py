import pygame
from Gun import Gun
from math import atan2, degrees, cos, sin, radians
pygame.init()

screen = pygame.display.set_mode((640, 480))

running = True
clock = pygame.time.Clock()
gun = Gun(320, 240)
gun_group = pygame.sprite.Group()
gun_group.add(gun)


def get_angle(x2, y2, x1, y1):
    dx = x1 - x2
    dy = y1 - y2
    rads = atan2(-dy, dx)
    return degrees(rads)

rectx = 0
recty = 0
angle = radians(-90)
while running:
    keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    recty -= sin(angle) * 100 * dt
    rectx += cos(angle) * 100 * dt

    degs = get_angle(gun.rect.centerx, gun.rect.centery, mouse_x, mouse_y)
    gun_group.update(mouse_x, mouse_y, degs)
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (int(rectx), int(recty), 10, 10))
    gun_group.draw(screen)
    pygame.display.flip()
pygame.quit()
