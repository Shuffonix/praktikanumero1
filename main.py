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
obstacles = pygame.sprite.Group()


def get_angle(x2, y2, x1, y1):
    dx = x1 - x2
    dy = y1 - y2
    rad = atan2(-dy, dx)
    return rad


top_border = Border(10, 10, 620, 0, 10)
left_border = Border(10, 10, 460, 90, 10)
right_border = Border(620, 10, 460, 90, 10)
bottom_border = Border(10, 460, 620, 0, 10)
for border in [top_border, left_border, right_border, bottom_border]:
    borders.add(border)

# huiasin sellega mingi 2h, ei saanud head tulemit random genereerimisega, võid vaadata üle kui tahad
map_selection = [[[50, 250], [400, 200], [300, 350]],
                 [[300, 350], [450, 50], [400, 150], [500, 50], [150, 150]],
                 [[250, 50], [450, 350], [150, 150]],
                 [[400, 200], [50, 300], [50, 50], [500, 350]],
                 [[100, 200], [350, 150], [50, 350]],
                 [[500, 300], [350, 250], [450, 100], [200, 50], [200, 350]],
                 [[100, 100], [400, 50], [500, 50], [50, 300], [400, 50], [350, 150], [350, 150]]
                 ]

# genereerib need plokkid maailma, kasutades grid süsteemi, ettevalitud listist, sest ma ei saanud seda muidu TÖÖÖLE!
nr = random.randint(0, len(map_selection)-1)
for l in map_selection[nr]:
    left_border = Border(l[0], l[1], 50, 90, 1)
    right_border = Border(l[0]+50, l[1], 50, 90, 1)
    top_border = Border(l[0], l[1], 50, 0, 1)
    bottom_border = Border(l[0], l[1]+50, 50, 0, 1)
    for border in [top_border, left_border, right_border, bottom_border]:
        borders.add(border)
    #new_obj = Obstacle(l[0], l[1])
    #obstacles.add(new_obj)


# katkine idee
"""while len(map_of_obstacles) < 2:

    x_cord = random.randint(90, screen.get_height() - 50)
    y_cord = random.randint(50, screen.get_width() - 90)
    # new_obstacle = Obstacle(x_cord, y_cord)
    print(x_cord, y_cord)
    for obj in map_of_obstacles:
        print(map_of_obstacles)
        if (obj[1]+50+ 10) < x_cord and (obj[1] - 10) > x_cord:

            if (obj[1] + 10) > y_cord or (obj[1]+90 - 10) < y_cord:
                if x_cord not in player_box and y_cord not in player_box:
                    new_obstacle = Obstacle(x_cord, y_cord)

                    map_of_obstacles.append([new_obstacle.rect.x, new_obstacle.rect.y])
                    obstacles.add(new_obstacle)"""


while running:
    #print(obstacles)
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
