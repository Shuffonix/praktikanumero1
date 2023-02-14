import pygame


screen = pygame.display.set_mode((640, 480))
kell = pygame.time.Clock()
running = True
global_x = 0
global_y = 0
speed = 100
selected_x = 0
selected_y = 0
blocks = set()
selected_block = pygame.Surface(size=(42, 42))
selected_block.fill((255, 0, 0))
selected_block.set_colorkey((255, 0, 0))
pygame.draw.rect(selected_block, (0, 0, 0), (0, 0, 42, 42), 3)
timer = 1
while running:
    hiire_x, hiire_y = pygame.mouse.get_pos()
    dt = kell.tick(60) / 1000
    keys = pygame.key.get_pressed()

    selected_x = hiire_x // 40 * 40 - global_x % 40 + 2
    selected_y = hiire_y // 40 * 40 - global_y % 40 + 2

    if not 0 < hiire_y - selected_y < 40:
        if hiire_y - selected_y > 40:
            selected_y += 40
        else:
            selected_y -= 40

    if not 0 < hiire_x - selected_x < 40:
        if hiire_x - selected_x > 40:
            selected_x += 40
        else:
            selected_x -= 40

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                blocks.add((selected_x-1, selected_y-1))
    if keys[pygame.K_d]:
        global_x += speed * dt
    if keys[pygame.K_a]:
        global_x -= speed * dt
    if keys[pygame.K_s]:
        global_y += speed * dt
    if keys[pygame.K_w]:
        global_y -= speed * dt

    # background
    screen.fill((255, 255, 255))
    for bg_x in range(-80 - int(global_x % 80), 720, 20):
        pygame.draw.line(screen, (225, 225, 225), (bg_x, 0), (bg_x, 480), 2)
    for bg_y in range(-80 - int(global_y % 80), 560, 20):
        pygame.draw.line(screen, (225, 225, 225), (0, bg_y), (640, bg_y), 2)
    # siit alates saab lisada blocke jms

    for block1, block2 in blocks:
        pygame.draw.rect(screen, (150, 255, 150), (block1, block2, 40, 40))
    screen.blit(selected_block, (selected_x - 2, selected_y - 2))

    pygame.display.flip()
pygame.quit()
