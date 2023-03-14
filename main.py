import pygame
from Block import Block
from Player import Player
pygame.init()


running = True
screen = pygame.display.set_mode((640, 480))
kell = pygame.time.Clock()
speed = 150
in_range = False
is_jumping = False
jump_cd = 0
global_x = 0  # x mis ei liigu mapi suhtes
global_y = 0  # y mis ei liigu mapi suhtes
local_x = 0  # 40ga ümardatud x ekraani suhtes
local_y = 0  # 40ga ümardatud y ekraani suhtes
selected_x = 0  # local_x aga mapi suhtes
selected_y = 0  # local_y aga mapi suhtes
vel_x = 0  # horisontaalkiirus
vel_y = 0  # vertikaalkiirus

# pmst (local_x, local_y) valikukasti jaoks,
# global_x/y + local_x/y = selected_x/y,
# (selected_x, selected_y) ülejäänud blockide jaoks

# kuna mängija püsib paigal ja map liigub,
# igasugused kiirused mängija pos liitmise asemel lahutatakse globalist
# (mängija "edasi liikumise" kujutamiseks liigub map tagasi)

# hiirt järgiv valikukast
selected_block = pygame.Surface(size=(42, 42))
selected_block.fill((255, 0, 0))
selected_block.set_colorkey((255, 0, 0))
pygame.draw.rect(selected_block, (0, 0, 0), (0, 0, 42, 42), 3)

# genereerib mapi
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)
blocks_dict = {}
blocks = pygame.sprite.Group()
for y in range(320, 2300, 40):
    for x in range(-1000, 1000, 40):
        block = Block(x, y)
        blocks_dict[block.id] = block
        blocks.add(block)
visible_blocks = pygame.sprite.Group()
# update(...) - uuendab blockide asukohti
# update(..., True) - uuendab lisaks ka naabreid (kasulik, kui lisad või eemaldad blocke)
blocks.update(global_x, global_y, blocks_dict, visible_blocks, True)


def detect_collision(vel_x, vel_y):
    global global_x, global_y, is_jumping
    vel_x = int(vel_x)
    vel_y = int(vel_y)
    up_points = [
        (player.rect.left, player.rect.top + vel_y - 1),
        (player.rect.right, player.rect.top + vel_y - 1)
    ]
    down_points = [
        (player.rect.left, player.rect.bottom + vel_y + 1),
        (player.rect.right, player.rect.bottom + vel_y + 1)
    ]
    left_points = [
        (player.rect.left + vel_x - 1, player.rect.top),
        (player.rect.left + vel_x - 1, player.rect.centery),
        (player.rect.left + vel_x - 1, player.rect.bottom)
    ]
    right_points = [
        (player.rect.right + vel_x + 1, player.rect.top),
        (player.rect.right + vel_x + 1, player.rect.centery),
        (player.rect.right + vel_x + 1, player.rect.bottom)
    ]

    moved = False
    for colliding_block in visible_blocks:
        if moved:
            break
        if vel_x > 0:
            for point in right_points:
                if colliding_block.rect.collidepoint(point):
                    global_x += colliding_block.rect.left - point[0] - 1
                    moved = True
                    break
        elif vel_x < 0:
            for point in left_points:
                if colliding_block.rect.collidepoint(point):
                    global_x += colliding_block.rect.right - point[0]
                    moved = True
                    break
        elif vel_y > 0:
            for point in down_points:
                if colliding_block.rect.collidepoint(point):
                    global_y += colliding_block.rect.top - point[1] - 1
                    moved = True
                    break
        elif vel_y < 0:
            for point in up_points:
                if colliding_block.rect.collidepoint(point):
                    global_y += colliding_block.rect.bottom - point[1]
                    moved = True
                    break

    if any(colliding.rect.collidepoint(point) for point in down_points for colliding in visible_blocks):
        is_jumping = False
    else:
        is_jumping = True


while running:
    hiire_x, hiire_y = pygame.mouse.get_pos()
    dt = kell.tick(144) / 1000
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    # horisontaalne liikumine
    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) == (keys[pygame.K_a] or keys[pygame.K_LEFT]):
        vel_x = 0
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        vel_x = -speed * dt
    else:
        vel_x = speed * dt

    # vertikaalne liikumine
    jump_cd -= dt
    if not is_jumping:
        vel_y = 0
        if jump_cd <= 0 and (keys[pygame.K_w] or keys[pygame.K_SPACE] or keys[pygame.K_UP]):
            vana = vel_y
            vel_y = -1000 * dt
            print(vana - vel_y)
            jump_cd = 1

    # mängija liikumine ja samaaegne collision detection blockidega
    detect_collision(vel_x, 0)
    global_x += vel_x

    detect_collision(0, vel_y)
    if is_jumping:
        vel_y += 20 * dt
        vel_y = min(vel_y, 100)
    global_y += vel_y

    if vel_x != 0 or vel_y != 0:
        blocks.update(global_x, global_y, blocks_dict, visible_blocks)

    left_click, middle_click, right_click = pygame.mouse.get_pressed()
    local_x = hiire_x // 40 * 40 - global_x % 40
    local_y = hiire_y // 40 * 40 - global_y % 40

    if not 0 < hiire_y - local_y < 40:
        if hiire_y - local_y > 40:
            local_y += 40
        else:
            local_y -= 40

    if not 0 < hiire_x - local_x < 40:
        if hiire_x - local_x > 40:
            local_x += 40
        else:
            local_x -= 40

    selected_x = 40 * round(int(global_x + local_x) / 40)
    selected_y = 40 * round(int(global_y + local_y) / 40)

    # raadius ekraani keskelt hiireni <= 200
    if ((hiire_x - 320)**2 + (hiire_y - 240)**2)**0.5 <= 200:
        in_range = True
    else:
        in_range = False

    # lõhub blocke
    # eeldused: block on olemas, on ulatuses
    if left_click:
        if (selected_x, selected_y) in blocks_dict and in_range:
            blocks_dict[(selected_x, selected_y)].kill()
            blocks_dict.pop((selected_x, selected_y))
            blocks.update(global_x, global_y, blocks_dict, visible_blocks, True)

    # lisab blocke
    # eeldused: on ulatuses, pole ees juba blocki, ei kattu mängijaga
    elif right_click:
        if in_range and not (selected_x, selected_y) in blocks_dict and not player.rect.colliderect(
                pygame.Rect(int(local_x), int(local_y), 40, 40)):
            block = Block(selected_x, selected_y)
            blocks.add(block)
            blocks_dict[block.id] = block
            blocks.update(global_x, global_y, blocks_dict, visible_blocks, True)

    # background
    screen.fill((255, 255, 255))
    for bg_x in range(-80 - int(global_x % 80), 720, 20):
        pygame.draw.line(screen, (225, 225, 225), (bg_x, 0), (bg_x, 480), 2)
    for bg_y in range(-80 - int(global_y % 80), 560, 20):
        pygame.draw.line(screen, (225, 225, 225), (0, bg_y), (640, bg_y), 2)
    # siit alates saab lisada blocke jms

    visible_blocks.draw(screen)
    player_group.draw(screen)

    # in range - valikukast
    # not in range - range circle
    if not in_range:
        pygame.draw.circle(screen, (125, 125, 125), (320, 240), 200, 2)
    elif (selected_x, selected_y) in blocks_dict:
        screen.blit(selected_block, (int(local_x), int(local_y)))
    pygame.display.flip()
pygame.quit()
