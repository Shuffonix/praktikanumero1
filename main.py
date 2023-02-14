import pygame


screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
running = True
character_x = 0
character_y = 0
speed = 100
kell = pygame.time.Clock()
mouse_x = 0
mouse_y = 0
while running:
    dt = kell.tick() / 1000
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_x = event.pos[0]//40 * 40
            mouse_y = event.pos[1]//40 * 40
    if keys[pygame.K_d]:
        character_x += speed * dt
    if keys[pygame.K_a]:
        character_x -= speed * dt
    if keys[pygame.K_s]:
        character_y += speed * dt
    if keys[pygame.K_w]:
        character_y -= speed * dt
    screen.fill((255, 255, 255))
    for bg_x in range(-80 - int(character_x % 80), 720, 20):
        pygame.draw.line(screen, (225, 225, 225), (bg_x, 0), (bg_x, 480), 2)
    for bg_y in range(-80 - int(character_y % 80), 560, 20):
        pygame.draw.line(screen, (225, 225, 225), (0, bg_y), (640, bg_y), 2)
    pygame.draw.rect(screen, (0, 0, 0), (mouse_x, mouse_y, 40, 40), 3)
    pygame.display.flip()
pygame.quit()
