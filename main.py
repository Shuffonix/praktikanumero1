import pygame
from gun import Gun
from bullet import Bullet
from border import Border
from math import atan2, degrees, cos, sin, radians
pygame.init()

screen = pygame.display.set_mode((640, 480))

running = True
clock = pygame.time.Clock()
gun = Gun(320, 240)
gun_group = pygame.sprite.Group()
gun_group.add(gun)
# hoiustan siin bulletid, ja lisan need loopi sees groupi
bullets = []


def check_collision_with_sides():
    # pmst mul on 4 külge ja ma kontrollin iga bulletiga kas ta on collisionis mõne küljega
    for bullet in bullets:
        obj = bullet.rect
        for x in borders:
            if obj.clipline(x.start, x.end):
                bullets.remove(bullet)
                print('hit!')
                break
    # kui bullet on collisionis, siis muuda kiirust vastandarvuks


def get_angle(x2, y2, x1, y1):
    dx = x1 - x2
    dy = y1 - y2
    rads = atan2(-dy, dx)
    return rads


borders = []
def draw_borders():
    border1 = Border(10, 10, screen.get_width() - 20, True)  # top
    border2 = Border(10, 10, screen.get_height() - 20, False)  # left
    border3 = Border(640 - 10, 0 + 10, screen.get_height() - 20, False)  # right
    border4 = Border(0 + 10, 480 - 10, screen.get_width() - 20, True)  # bottom
    borders.append(border1)
    borders.append(border2)
    borders.append(border3)
    borders.append(border4)
    for b in borders:
        b.draw(screen)



while running:
    screen.fill((255, 255, 255))
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dt = clock.tick() / 1000


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                degs = get_angle(gun.rect.centerx, gun.rect.centery, mouse_x, mouse_y)
                new_bullet = Bullet(320, 240, degs)
                bullets.append(new_bullet)

    degs = get_angle(gun.rect.centerx, gun.rect.centery, mouse_x, mouse_y)
    gun_group.update(mouse_x, mouse_y, degrees(degs))
    gun_group.draw(screen)

    draw_borders()
    # bulletide uuendamine
    for bullet in bullets:
        bullet.update(dt)
    check_collision_with_sides()
    # borders.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.flip()
pygame.quit()
