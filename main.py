import pygame
from gun import Gun
from bullet import Bullet
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



def get_angle(x2, y2, x1, y1):
    dx = x1 - x2
    dy = y1 - y2
    rads = atan2(-dy, dx)
    return rads

rectx = 0
recty = 0
angle1 = radians(-90)
angle2 = radians(-45)
while running:
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

    # bulletide uuendamine
    for bullet in bullets:
        bullet.update(dt)

    degs = get_angle(gun.rect.centerx, gun.rect.centery, mouse_x, mouse_y)
    gun_group.update(mouse_x, mouse_y, degrees(degs))

    screen.fill((255, 255, 255))
    gun_group.draw(screen)
    print(len(bullets))

    # bulletide renderdamine
    for bullet in bullets:
        if bullet.x > screen.get_width() or bullet.x < 0 or bullet.y > screen.get_height() or bullet.y < 0:
            bullets.remove(bullet)
        else:
            bullet.draw(screen)
    pygame.display.flip()
pygame.quit()
