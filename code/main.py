import pygame, sys
import pygame.freetype
import pytmx
from settings import *
from sprite import *
from player import *
from level import *
from debug import debug

# Draw the map
# def draw_map(tmx_data):
#     for layer in tmx_data.visible_layers:
#         if isinstance(layer, pytmx.TiledTileLayer):
#             for x, y, gid in layer:
#                 tile = tmx_data.get_tile_image_by_gid(gid)
#                 if tile:
#                     screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))      
        

# if __name__ == "__main__":
#     # Initialize Pygame
#     pygame.init()

#     # Screen
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
#     # Load the TMX map
#     tmx_data = pytmx.load_pygame("../data/level_design.tmx")
#     pygame.display.set_caption('Dungeons Game')


#     # Load background image
#     # bg_image = pygame.image.load('../data/level1-background.png')

#     player = Player(x_pos = 200, y_pos = 300)
    
    
#     # Main game loop
#     clock = pygame.time.Clock()
#     running = True

#     while running:

#         # Clear the screen
#         screen.fill((0, 0, 0))
#         # screen.blit(bg_image, (0, 0))
#         draw_map(tmx_data)
        
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
                
            

#         # Draw the sprite
#         # player.draw(screen)
#         # player.update_animation()
#         # player.x_pos += 1
#         # print(player.frame_index)
#         player.keypress_handler()
#         player.draw(screen=screen)
#         player.update_animation()
        
#         # Update the display
#         # pygame.time.delay(30)
#         pygame.display.update()
#         clock.tick(60)  # Limit to 60 FPS
        
#     pygame.quit()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Dungeon Escape')
        self.clock = pygame.time.Clock()
        self.level = Level()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('black')
            self.level.run()
            # debug('Test')
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()