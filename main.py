import pygame
import random
from gun import Gun
from bullet import Bullet
from border import Border
from explosion import Explosion
from enemy import Enemy
from math import atan2, degrees, cos, sin
pygame.init()


screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
running = True
character_x = 0
character_y = 0
speed = 100

screen = pygame.display.set_mode((640, 480))
background = pygame.image.load("star_background.png")
gun_sound = pygame.mixer.Sound("sounds/gun_fire.wav")
wall_bang_sound = pygame.mixer.Sound("sounds/bullet_bounce.wav")
wall_bang_sound.set_volume(0.3)
game_end_sound = pygame.mixer.Sound("sounds/game_end.wav")
bullet_explode_sound = pygame.mixer.Sound("sounds/bullet_explode.wav")
pygame.mixer.set_num_channels(20)


kell = pygame.time.Clock()
speed = 100
in_range = False

running = True
clock = pygame.time.Clock()
gun = Gun(320, 240)
gun_group = pygame.sprite.Group()
gun_group.add(gun)

# hoiustan siin aktiivseid kuule
bullets = pygame.sprite.Group()
# hoiustan particleid mis tekivad kui kuul liiga palju bouncib
bounce_particles = []
death_particles = pygame.sprite.Group()

# mängu borderid
borders = pygame.sprite.Group()

# enemies
enemies = pygame.sprite.Group()
enemies.add(Enemy(350, 350))

def time_to_size(particle_time):
    if particle_time > 0.9:
        return max(int(300 * (1 - particle[0])), 1)
    elif particle_time > 0.7:
        return 30
    else:
        return max(int((30 / 0.7) * particle[0]), 1)


def get_angle(x2, y2, x1, y1):
    dx = x1 - x2
    dy = y1 - y2
    rad = atan2(-dy, dx)
    return rad

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

top_border = Border(10, 10, 620, 0)
left_border = Border(10, 10, 460, 90)
right_border = Border(620, 10, 460, 270)
bottom_border = Border(10, 460, 620, 180)
for border in [top_border, left_border, right_border, bottom_border]:
    borders.add(border)

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

    mouse_presses = pygame.mouse.get_pressed()
    if mouse_presses[0]:
        now = pygame.time.get_ticks()
        if now - gun.last_shot > 500:
            gun.last_shot = now
            new_bullet = Bullet(rads)
            bullets.add(new_bullet)
            gun_sound.play()

    screen.blit(background, (0, 0))
    gun_group.update(mouse_x, mouse_y, degrees(rads), screen)

    for bullet in bullets:
        particles_raw = bullet.update(dt, borders, enemies, screen)
        if particles_raw:
            for particle in particles_raw:
                if not particle[3]:
                    bounce_particles.append(particle)
                    wall_bang_sound.play()
                else:
                    death = Explosion(particle[2], 100)
                    death_particles.add(death)
                    bullet_explode_sound.play()

    death_particles.update()
    # ekraanile joonistamine

    bullets.draw(screen)
    gun_group.draw(screen)
    enemies.draw(screen)
    screen.blit(gun.cd_overlay, gun.cd_rect)
    borders.draw(screen)

    for particle in bounce_particles[:]:
        if particle[0] < 0:
            bounce_particles.remove(particle)
            continue
        pygame.draw.circle(screen, (170, 170, 170), particle[2], int(particle[0] * 100))
        pygame.draw.circle(screen, (0, 0, 0), particle[2], int(particle[0] * 100), 1)
        particle[2][0] += dt * 400 * cos(particle[1])
        particle[2][1] += dt * 400 * -sin(particle[1])
        particle[0] -= 0.5 * dt

    death_particles.draw(screen)
    pygame.display.update()

pygame.quit()
