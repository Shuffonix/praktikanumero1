import pygame
from Block import Block


screen = pygame.display.set_mode((640, 480))
kell = pygame.time.Clock()
speed = 100
in_range = False
running = True
global_x = 0  # x mis ei liigu mapi suhtes
global_y = 0  # y mis ei liigu mapi suhtes
local_x = 0  # 40ga ümardatud x ekraani suhtes
local_y = 0  # 40ga ümardatud y ekraani suhtes
selected_x = 0  # local_x aga mapi suhtes
selected_y = 0  # local_y aga mapi suhtes

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
blocks_dict = {}
blocks = pygame.sprite.Group()
for y in range(320, 2300, 40):
    for x in range(-1000, 1000, 40):
        block = Block(x, y)
        blocks_dict[block.id] = block
        blocks.add(block)

# update(...) - uuendab blockide asukohti
# update(..., True) - uuendab lisaks ka naabreid (kasulik, kui lisad või eemaldad blocke)
blocks.update(global_x, global_y, blocks_dict, True)

while running:
    hiire_x, hiire_y = pygame.mouse.get_pos()
    dt = kell.tick(144) / 1000
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:  # liigu
        global_x += speed * dt
    if keys[pygame.K_a]:
        global_x -= speed * dt
    if keys[pygame.K_s]:
        global_y += speed * dt
    if keys[pygame.K_w]:
        global_y -= speed * dt

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # lõhub blocke
    if left_click:
        if (selected_x, selected_y) in blocks_dict and in_range:
            blocks_dict[(selected_x, selected_y)].kill()
            blocks_dict.pop((selected_x, selected_y))
            blocks.update(global_x, global_y, blocks_dict, True)

    # lisab blocke
    elif right_click:
        if (not (selected_x, selected_y) in blocks_dict) and in_range:
            block = Block(selected_x, selected_y)
            blocks.add(block)
            blocks_dict[block.id] = block
            blocks.update(global_x, global_y, blocks_dict, True)

    # background
    screen.fill((255, 255, 255))
    for bg_x in range(-80 - int(global_x % 80), 720, 20):
        pygame.draw.line(screen, (225, 225, 225), (bg_x, 0), (bg_x, 480), 2)
    for bg_y in range(-80 - int(global_y % 80), 560, 20):
        pygame.draw.line(screen, (225, 225, 225), (0, bg_y), (640, bg_y), 2)
    # siit alates saab lisada blocke jms

    blocks.update(global_x, global_y, blocks_dict)
    blocks.draw(screen)

    # in range - valikukast
    # not in range - range circle
    if not in_range:
        pygame.draw.circle(screen, (125, 125, 125), (320, 240), 200, 2)
    elif (selected_x, selected_y) in blocks_dict:
        screen.blit(selected_block, (local_x, local_y))
    pygame.display.flip()
pygame.quit()
