import pygame
from gun import Gun
from bullet import Bullet
from border import Border
from math import atan2, degrees, cos, sin, radians, pi
pygame.init()

screen = pygame.display.set_mode((640, 480))

running = True
clock = pygame.time.Clock()
gun = Gun(320, 240)
gun_group = pygame.sprite.Group()
gun_group.add(gun)

# hoiustan siin aktiivseid kuule
bullets = []
# hoiustan particleid mis tekivad kui kuul liiga palju bouncib
particles = []
# mängu borderid
borders = []

def check_border_collision():
    global particles
    # pmst mul on 4 külge ja ma kontrollin iga bulletiga kas ta on collisionis mõne küljega
    for bullet in bullets:
        obj = bullet.rect
        for x in borders:
            if obj.clipline(x.start, x.end):
                # kui bullet on collisionis, siis muuda kiirust vastandarvuks, sellega saab vastupidise liikumise suuna
                if bullet.bounces > 3:
                    particles = bullet.explode()
                    bullets.remove(bullet)
                bullet.velocity *= -1
                bullet.bounces += 1
                # lisan 90 deg, sest nii peaks vist saama peegeldusnurga???
                bullet.rad += pi/2
                bullet.update_angle()
                break


def get_angle(x2, y2, x1, y1):
    dx = x1 - x2
    dy = y1 - y2
    rads = atan2(-dy, dx)
    return rads


def draw_borders():
    border1 = Border(10, 10, screen.get_width() - 20, True)  # top
    border2 = Border(10, 10, screen.get_height() - 20, False)  # left
    border3 = Border(screen.get_width() - 10, 0 + 10, screen.get_height() - 20, False)  # right
    border4 = Border(0 + 10, screen.get_height() - 10, screen.get_width() - 20, True)  # bottom
    borders.append(border1)
    borders.append(border2)
    borders.append(border3)
    borders.append(border4)
draw_borders()


while running:
    screen.fill((255, 255, 255))
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # selle teeb veel paremaks, see hetkel ainult nii lol
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                degs = get_angle(gun.rect.centerx, gun.rect.centery, mouse_x, mouse_y)
                new_bullet = Bullet(320, 240, degs)
                bullets.append(new_bullet)

    degs = get_angle(gun.rect.centerx, gun.rect.centery, mouse_x, mouse_y)
    gun_group.update(mouse_x, mouse_y, degrees(degs))
    gun_group.draw(screen)

    # joonistan borderid ekraanile siin
    for b in borders:
        b.draw(screen)

    # bulletide uuendamine
    for bullet in bullets:
        bullet.update(dt)

    #check_border_collision()

    # particles renderdamine
    for i in range(8):
        if len(particles) == 0:  # säästame CPU-d
            break

        for p in particles:
            p.move()
            pygame.draw.circle(screen, (255, 0, 0), (p.x, p.y), 8-i)

    if len(particles) > 0:
        particles.pop(0)

    # bulletide ekraanile joonistamine
    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.update()
pygame.quit()
