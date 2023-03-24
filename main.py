import pygame
from gun import Gun
from bullet import Bullet
from border import Border
from math import atan2, degrees
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


<<<<<<< HEAD
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

=======
top_border = Border(10, 10, 620, 0)
left_border = Border(10, 10, 460, 90)
right_border = Border(620, 10, 460, 90)
bottom_border = Border(10, 460, 620, 0)
for border in [top_border, left_border, right_border, bottom_border]:
    borders.add(border)
>>>>>>> trevori-branch

while running:
    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
<<<<<<< HEAD
    dt = clock.tick(60) / 1000
=======
    dt = clock.tick(144) / 1000
    rads = get_angle(gun.rect.centerx, gun.rect.centery, mouse_x, mouse_y)
>>>>>>> trevori-branch

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
    bullets.update(dt, borders)

    # ekraanile joonistamine
    bullets.draw(screen)
    gun_group.draw(screen)
<<<<<<< HEAD

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
=======
    borders.draw(screen)
>>>>>>> trevori-branch

    pygame.display.update()
pygame.quit()
