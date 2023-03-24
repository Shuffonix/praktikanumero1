import pygame
from gun import Gun
from bullet import Bullet
from border import Border
from math import atan2, degrees, pi
pygame.init()

screen = pygame.display.set_mode((640, 480))

running = True
clock = pygame.time.Clock()
gun = Gun(320, 240)
gun_group = pygame.sprite.Group()
gun_group.add(gun)

# hoiustan siin aktiivseid kuule
bullets = pygame.sprite.Group()
# hoiustan particleid mis tekivad kui kuul liiga palju bouncib
particles = []
# mängu borderid
borders = pygame.sprite.Group()


def get_angle(x2, y2, x1, y1):
    dx = x1 - x2
    dy = y1 - y2
    rad = atan2(-dy, dx)
    return rad


top_border = Border(10, 10, 620, 0)
left_border = Border(10, 10, 460, 90)
right_border = Border(620, 10, 460, 90)
bottom_border = Border(10, 460, 620, 0)
for border in [top_border, left_border, right_border, bottom_border]:
    borders.add(border)

while running:
    screen.fill((255, 255, 255))
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dt = clock.tick(144) / 1000
    rads = get_angle(gun.rect.centerx, gun.rect.centery, mouse_x, mouse_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # selle teeb veel paremaks, see hetkel ainult nii lol
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                new_bullet = Bullet(rads)
                bullets.add(new_bullet)

    gun_group.update(mouse_x, mouse_y, degrees(rads))
    bullets.update(dt)

    # ekraanile joonistamine
    bullets.draw(screen)
    gun_group.draw(screen)
    borders.draw(screen)

    pygame.display.update()
pygame.quit()
