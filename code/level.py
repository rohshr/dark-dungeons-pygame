import pygame
from settings import *
from player import Player
from tile import Tile
import pytmx
from pytmx.util_pygame import load_pygame
from debug import debug
from support import *

class Level:
    def __init__(self):
        
        # get the display surface
        self.display_surface = pygame.display.get_surface() # defined in main.py; gets display surface from anywhere in the code

        # sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        self.tmx_data = load_pygame('../data/level_design.tmx')
        
        self.create_map()
        # print("test")               
        # self.get_layer()
        
    
    # def setup(self):
    #     # self.player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    #     for row in tmx_data:
    #         print(row)
    
    # Get TMX layer
    def get_layer_tiles(self, layer_name):
        tile_images = []
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                if layer.name == layer_name:
                    for x, y, gid in layer:
                        # tile_img = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                        tile_img = self.tmx_data.get_tile_image_by_gid(gid)
                        # print(tile_img)
                        if tile_img:
                            temp_img = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                            temp_img.blit(tile_img.convert_alpha(), (0, 0), tile_img.get_rect())
                            temp_img.set_colorkey('black')
                            tile_images.append(temp_img)
        return(tile_images)
                            
    
    
    # Draw the map
    def create_map(self):
        # for layer in self.tmx_data.visible_layers:
        #     if isinstance(layer, pytmx.TiledTileLayer):
        #         for x, y, gid in layer:
        #             tile_img = self.tmx_data.get_tile_image_by_gid(gid)
        #             if tile_img:
        #                 # self.display_surface.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight)) 
        #                 if layer.name == 'Walls':
        #                     self.walls = Tile(tile_img, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), [self.visible_sprites, self.collision_sprites])
        #                 elif layer.name == 'Floor':
        #                     Tile(tile_img, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), [self.visible_sprites])

        layout = {
            'boundary': import_csv_layout('../map/level_design_FloorBlocks.csv'),
            'walls': import_csv_layout('../map/level_design_Walls.csv'),
            'objects': import_csv_layout('../map/level_design_Dungeon Interior.csv')
        }
        
        graphics = {
            'walls' : self.get_layer_tiles('Walls'),
            'objects' : self.get_layer_tiles('Dungeon Interior')
        }
        
        for style, layout in layout.items():
            i = 0
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if style == 'boundary':
                            Tile((x, y), self.collision_sprites, 'invisible')
                        elif style == 'walls':
                            # print(graphics['walls'])
                            Tile((x, y), [self.visible_sprites, self.collision_sprites], 'walls', graphics['walls'][i])
                            i += 1
                        elif style == 'objects':
                            Tile((x, y), [self.visible_sprites, self.collision_sprites], 'objects', graphics['objects'][i])
                            i += 1
                            
                            # for tile in graphics['walls']:
                            #     Tile((x, y), self.collision_sprites, 'walls', tile)

                            
        self.player = Player((1200, 1000), [self.visible_sprites], self.collision_sprites, spritesheet_image_file = '../graphics/dungeon_hero_sprites.png')
        
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        # self.visible_sprites.create_map()
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    '''Class for camera; sprites sorted by Y coordinates'''
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.screen_width = self.display_surface.get_size()[0]
        self.screen_height = self.display_surface.get_size()[1]
        self.offset = pygame.math.Vector2() # offsets the map and view
        
        
        # creating floor
        self.floor_surf = pygame.image.load('../graphics/tilemap/floor.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
        
        
    def custom_draw(self, player):
        
        # getting offset form the player
        self.offset.x = player.rect.centerx - self.screen_width // 2
        self.offset.y = player.rect.centery - self.screen_height // 2
        
        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image.convert_alpha(), offset_pos)
            