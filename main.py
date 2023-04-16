import pygame
import random
from math import atan2, degrees, cos, sin

from gun import Gun
from bullet import Bullet
from border import Border
from explosion import Explosion
from enemy import Enemy

pygame.init()

font = pygame.font.Font('assets/aesymatt.ttf', 24)
screen = pygame.display.set_mode((640, 530))

background = pygame.image.load("assets/star_background.png")
title = pygame.image.load("assets/title_icon.png")
title_rect = title.get_rect(center=(320, 70))
newgame_button = pygame.image.load("assets/newgame_button.png")
newgame_rect = newgame_button.get_rect(center=(150, 400))
return_button = pygame.image.load("assets/returnmenu.png")
return_rect = return_button.get_rect(center=(150, 400))
death_msg = pygame.image.load("assets/deathmessage.png")
death_rect = death_msg.get_rect(center=(320, 70))
heart = pygame.image.load("assets/heart.png")
heart = pygame.transform.scale(heart, (50, 50))


gun_sound = pygame.mixer.Sound("sounds/gun_fire.wav")
gun_sound.set_volume(0.5)
wall_bang_sound = pygame.mixer.Sound("sounds/bullet_bounce.wav")
wall_bang_sound.set_volume(0.2)
game_end_sound = pygame.mixer.Sound("sounds/game_end.wav")
game_end_sound.set_volume(0.5)
bullet_explode_sound = pygame.mixer.Sound("sounds/bullet_explode.wav")
bullet_explode_sound.set_volume(0.5)
pygame.mixer.set_num_channels(20)

running = True
menu = True
ingame = False
endgame = False

clock = pygame.time.Clock()


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


# genereerib need plokkid maailma, kasutades grid süsteemi, ettevalitud listist, sest ma ei saanud seda muidu tööle
def obstacle_generation():
    global nr
    nr = random.randint(0, len(map_selection)-1)
    border_list = []
    for l in map_selection[nr]:
        left_border = Border(l[0]-3, l[1]+1, 49, 270, 2)
        border_list.append(left_border)

        right_border = Border(l[0]+50, l[1] + 1, 49, 90, 1)
        border_list.append(right_border)

        top_border = Border(l[0], l[1], 50, 180, 2)
        border_list.append(top_border)

        bottom_border = Border(l[0]+1, l[1]+48, 50, 0, 2)
        border_list.append(bottom_border)
    return border_list


# Outer borderid
top_border = Border(10, 10, 620, 0)
left_border = Border(10, 10, 460, 90)
right_border = Border(620, 10, 460, 270)
bottom_border = Border(10, 460, 620, 180)
mainseinad = [top_border, left_border, right_border, bottom_border]


# Enemy AI
def generate_enemy_grid():
    global nr
    # enemy spawnimise süsteem
    dont_spawn = [[250, 200], [250, 250], [300, 200], [300, 200], [300, 250]]  # arvestasin playeri dimensioonid siia sisse
    spawn_area = []

    for x in range(50, 550, 50):
        for y in range(50, 450, 50):
            if [x, y] not in map_selection[nr] and [x, y] not in dont_spawn:
                spawn_area.append([x, y])

    return spawn_area


spawn_area = []  # ala, kuhu saab enemy spawnida, arvutatakse välja iga kord kui hakatakse mängima


def generate_enemy():
    return random.choice(spawn_area)


# UI elements
score_board = pygame.Surface((640, 60))


def update_scoreboard(score):
    score_board.fill((0, 0, 0))
    if score > 1000:
        text_surface = font.render(f'Score: {round(score/1000, 2)}k', True, (255, 255, 255))
    else:
        text_surface = font.render(f'Score: {score}', True, (255, 255, 255))
    score_board.blit(text_surface, dest=(10, 25))


lives_board = pygame.Surface((400, 60))


def update_lives():
    lives_board.fill((0, 0, 0))
    for i in range(lives):
        lives_board.blit(heart, dest=(300-i*60, 10))


while running:
    # Esimenüü jaoks vajalikud asjad
    bullets = pygame.sprite.Group()  # hoiustan siin aktiivseid kuule
    bounce_particles = []  # hoiustan particleid mis tekivad kui kuul liiga palju bouncib
    death_particles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    sceduled_enemies = []

    gun_group = pygame.sprite.Group()
    gun = Gun(320, 240)
    gun_group.add(gun)

    borders = pygame.sprite.Group()
    for border in mainseinad:
        borders.add(border)

    bullet = False
    score = 0
    lives = 3
    hit_time = 0

    while menu:
        dt = clock.tick(144) / 1000
        screen.fill((0, 0, 0))
        screen.blit(title, title_rect)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rads = get_angle(gun.rect.centerx, gun.rect.centery, mouse_x, mouse_y)
        gun_group.update(mouse_x, mouse_y, degrees(rads), screen)

        gun_group.draw(screen)
        screen.blit(gun.cd_overlay, gun.cd_rect)
        screen.blit(newgame_button, newgame_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                running = False
                break
        mouse_presses = pygame.mouse.get_pressed()
        if newgame_rect.collidepoint(pygame.mouse.get_pos()) and not bullet:
            if mouse_presses[0]:
                now = pygame.time.get_ticks()
                if now - gun.last_shot > 500:
                    gun.last_shot = now
                    bullet = Bullet(rads)
                    bullets.add(bullet)
                    gun_sound.play()

        if bullet:
            bullet.update(dt, borders, enemies, screen)
            bullets.draw(screen)
            if bullet.rect.colliderect(newgame_rect):
                menu = False
                ingame = True
                death_particles.add(Explosion(newgame_rect.center, 250))

        pygame.display.update()
    obstacles = obstacle_generation()
    for obstacle in obstacles:
        borders.add(obstacle)
    spawn_area = generate_enemy_grid()
    bullet.kill()

    # Mängu osa
    while ingame:
        # print(generate_rectangles)

        screen.fill((0, 0, 0))

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dt = clock.tick(144) / 1000
        rads = get_angle(gun.rect.centerx, gun.rect.centery, mouse_x, mouse_y)
        mouse_presses = pygame.mouse.get_pressed()

        # UI uuendamine
        update_scoreboard(score)
        update_lives()
        screen.blit(score_board, dest=(0, 460))
        screen.blit(lives_board, dest=(280, 465))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ingame = False
                running = False
                break

        if mouse_presses[0]:
            now = pygame.time.get_ticks()
            if now - gun.last_shot > 500:
                gun.last_shot = now
                new_bullet = Bullet(rads)
                bullets.add(new_bullet)
                gun_sound.play()

        screen.blit(background, (0, 0))
        gun_group.update(mouse_x, mouse_y, degrees(rads), screen)

        # Playeri surm, elude süsteem, reaktsioon
        if hit_time != 0 and pygame.time.get_ticks() - hit_time > 2000:  # mingi aeg kui kaua ta on punane
            gun.hit = False

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
                        score += bullet.return_score()

            if pygame.sprite.collide_mask(gun, bullet):
                if bullet.collisions > 0:
                    bullet_explode_sound.play()
                    bullet.kill()
                    gun.hit = True
                    hit_time = pygame.time.get_ticks()
                    lives -= 1


                if lives == 0:
                    ingame = False
                    endgame = True
                    pygame.mixer.stop()
                    game_end_sound.play()
                    break

        death_particles.update()
        enemies.update(dt, bullets)

        # enemy spawnimise loogika
        if random.randint(1, 100) == 50 and len(enemies) < 2:
            for i in range(random.randint(1, 3)):
                x, y = generate_enemy()
                sceduled_enemies.append(Enemy(x, y, round(random.uniform(0.75, 1.2), 2)))
        if random.randint(1, 100) % 17 == 0 and len(sceduled_enemies):
            enemies.add(sceduled_enemies[0])
            sceduled_enemies.pop(0)

        # Asjade ekraanile panemine
        enemies.draw(screen)
        bullets.draw(screen)
        gun_group.draw(screen)
        screen.blit(gun.cd_overlay, gun.cd_rect)
        borders.draw(screen)

        # Blokkide ära fillimine
        for x, y in map_selection[nr]:
            pygame.draw.rect(screen, (255, 255, 255), (x, y, 51, 50))

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

    for bullet in bullets:
        bullet.kill()
    for obstacle in obstacles:
        obstacle.kill()
    bullet = False
    hit_time = 0
    while endgame:
        dt = clock.tick(144) / 1000
        screen.fill((0, 0, 0))
        screen.blit(return_button, return_rect)
        screen.blit(death_msg, death_rect)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rads = get_angle(gun.rect.centerx, gun.rect.centery, mouse_x, mouse_y)
        gun_group.update(mouse_x, mouse_y, degrees(rads), screen)
        gun_group.draw(screen)
        screen.blit(gun.cd_overlay, gun.cd_rect)
        # borders.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endgame = False
                running = False
                ingame = False
                break
        mouse_presses = pygame.mouse.get_pressed()
        if return_rect.collidepoint(pygame.mouse.get_pos()) and not bullet:
            if mouse_presses[0]:
                now = pygame.time.get_ticks()
                if now - gun.last_shot > 500:
                    gun.last_shot = now
                    bullet = Bullet(rads)
                    bullets.add(bullet)
                    gun_sound.play()
        if bullet:
            bullet.update(dt, borders, enemies, screen)
            bullets.draw(screen)
            if bullet.rect.colliderect(return_rect):
                menu = True
                endgame = False
                death_particles.add(Explosion(return_rect.center, 250))
        pygame.display.update()
pygame.quit()
