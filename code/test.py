import pygame
import pytmx

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1024, 768))

# Load the TMX map
tmx_data = pytmx.load_pygame("Assets/level_design.tmx")

# Draw the map
def draw_map(tmx_data):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_map(tmx_data)
    pygame.display.flip()

pygame.quit()