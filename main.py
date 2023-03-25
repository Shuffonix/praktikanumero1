import pygame
import random
from gun import Gun
from bullet import Bullet
from border import Border
from obstacle import Obstacle
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
# mingid teised obstacles
map_of_obstacles = []
obstacles = pygame.sprite.Group()


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


new_obstacle = Obstacle(random.randint(90, screen.get_height() - 90), random.randint(50, screen.get_width() - 50))
map_of_obstacles.append([new_obstacle.width, new_obstacle.rect.x, new_obstacle.rect.y])
obstacles.add(new_obstacle)
player_box = (420, 240+190)

# genereerib need plokkid maailma
while len(map_of_obstacles) < 3:

    x_cord = random.randint(90, screen.get_height() - 50)
    y_cord = random.randint(50, screen.get_width() - 90)

    for obj in map_of_obstacles:

        if (obj[1]+50+ 10) > x_cord and (obj[1]+50 - 10) < x_cord:
            if (obj[0]+90 + 10) > y_cord and (obj[0]+90 - 10) < y_cord:
                if x_cord not in player_box and y_cord not in player_box:
                    new_obstacle = Obstacle(x_cord, y_cord)

                    map_of_obstacles.append([new_obstacle.rect.x, new_obstacle.rect.y])
                    obstacles.add(new_obstacle)


while running:
    screen.fill((0, 0, 0))
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
    bullets.update(dt, borders, obstacles)

    # ekraanile joonistamine
    bullets.draw(screen)
    gun_group.draw(screen)
    borders.draw(screen)
    obstacles.draw(screen)

    pygame.display.update()
pygame.quit()
