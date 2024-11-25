import pygame
from settings import *
from player import Player
from enemy import Enemy
from tile import Tile
import pytmx
from pytmx.util_pygame import load_pygame
from debug import debug
from support import *
from ui import *
import random

class Level:
    def __init__(self):
        
        # get the display surface
        self.display_surface = pygame.display.get_surface() # defined in main.py; gets display surface from anywhere in the code
        self.screen_width = self.display_surface.get_size()[0]
        self.screen_height = self.display_surface.get_size()[1]

        # sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tmx_data = load_pygame('../data/level_design.tmx')
        
        # setup sprites
        self.create_map()
        
        # user interface
        self.ui = UI()
    
    # Get TMX layer
    def get_layer_tiles(self, layer_name, color_key=COLOR_KEY):
        tile_images = []
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                if layer.name == layer_name:
                    for x, y, gid in layer:
                        tile_img = self.tmx_data.get_tile_image_by_gid(gid)
                        if tile_img:
                            tile_img.set_colorkey(color_key)
                            tile_images.append(tile_img)
        return(tile_images)
    
    # Draw the map
    def create_map(self):
        # Load sprites for map from the TMX file
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_img = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile_img:
                        tile_img = tile_img.convert_alpha()
                        if layer.name == 'FloorBlocks':
                            self.walls = Tile((x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), self.collision_sprites, 'invisible')
                        elif layer.name == 'Walls':
                            tile_img.set_colorkey(COLOR_KEY)
                            self.walls = Tile((x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), [self.visible_sprites, self.collision_sprites], 'walls', tile_img)
                        elif layer.name == 'InnerWalls':
                            tile_img.set_colorkey('black')
                            self.walls = Tile((x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), [self.visible_sprites, self.collision_sprites], 'inner_walls', tile_img)
                        elif layer.name == 'DungeonEnvironment':
                            tile_img.set_colorkey('black')
                            Tile((x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), [self.visible_sprites, self.collision_sprites], 'objects', tile_img)
                        elif layer.name == 'Decorations':
                            tile_img.set_colorkey('black')
                            Tile((x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), self.visible_sprites, 'objects', tile_img)
                        elif layer.name == 'Enemies':
                            monster_name = random.choice([key for key in monster_data])
                            Enemy(monster_name, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), self.visible_sprites, self.collision_sprites, spritesheet_image_file = '../graphics/enemies.png')
                      
        self.player = Player((1000, 1000), self.visible_sprites, self.collision_sprites, spritesheet_image_file = '../graphics/dungeon_hero_sprites.png')
    
    def show_darkness(self, player):
        
        # darkness setup
        darkness_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        darkness_overlay = pygame.draw.rect(darkness_surface, 'white', (0, 0, self.screen_width, self.screen_height))
        
        # circle of vision in the center
        vision_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        circle_x, circle_y = self.screen_width // 2, self.screen_height // 2
        circle_radius = (300 if player.has_light else 100)
        
        vision_overlay = pygame.draw.circle(vision_surface, 'white', (circle_x, circle_y), circle_radius)
        
        mask_darkness = pygame.mask.from_surface(darkness_surface)
        mask_vision = pygame.mask.from_surface(vision_surface)
        mask_vision.invert()
        subtract_masks = mask_darkness.overlap_mask(mask_vision, (0, 0))
        
        subtract_shapes = subtract_masks.to_surface(darkness_surface, setcolor = 'black', unsetcolor = (0, 0, 0, 0))
        
        self.display_surface.blit(subtract_shapes, (0, 0))
    
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.show_darkness(self.player)
        self.ui.display(self.player)

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
        
        # getting offset from the player
        self.offset.x = player.rect.centerx - self.screen_width // 2 + player.rect.width // 2 # offset to the exact center of the player
        self.offset.y = player.rect.centery - self.screen_height // 2 + player.rect.height // 2
        # pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), player.hitbox, 2)
        
        
        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        