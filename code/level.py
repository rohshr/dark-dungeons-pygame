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
from weapon import Weapon
import random

class Level:
    def __init__(self):
        
        # get the display surface
        self.display_surface = pygame.display.get_surface() # defined in main.py; gets display surface from anywhere in the code
        self.screen_width = self.display_surface.get_size()[0]
        self.screen_height = self.display_surface.get_size()[1]
        self.game_paused = False
        self.game_exit = False

        # sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tmx_data = load_pygame('../data/level_design.tmx')
        
        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        
        # setup sprites
        self.create_map()
        
        # door status
        self.door_open = False
        
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
        self.item_locations = []
        self.door_location = []
        self.open_door_images = []
        key_img = pygame.image.load('../graphics/key.png').convert_alpha()
        sword_img = pygame.image.load('../graphics/sword.png').convert_alpha()
        lamp_img = pygame.image.load('../graphics/lamp.png').convert_alpha()
        # Load sprites for map from the TMX file
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_img = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile_img:
                        tile_img = tile_img.convert_alpha()
                        tile_img.set_colorkey(COLOR_KEY)
                        if layer.name == 'FloorBlocks':
                            Tile((x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), self.collision_sprites, 'invisible')
                        elif layer.name == 'Walls':
                            Tile((x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), [self.visible_sprites, self.collision_sprites], 'walls', tile_img)
                        elif layer.name == 'DoorClosed':
                            Tile((x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), [self.visible_sprites, self.collision_sprites], 'door_closed', tile_img)
                        elif layer.name == 'DoorActionArea':
                            Tile((x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), self.collision_sprites, 'door_action_area')
                        elif layer.name == 'DoorOpen':
                            tile_img.set_colorkey('black')
                            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                            self.door_location.append((x, y))
                            self.open_door_images.append(tile_img)
                        elif layer.name == 'Exit':
                            Tile((x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), self.collision_sprites, 'exit')
                        elif layer.name == 'InnerWalls':
                            tile_img.set_colorkey('black')
                            Tile((x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), self.collision_sprites, 'inner_walls')
                        elif layer.name == 'DungeonEnvironment':
                            tile_img.set_colorkey('black')
                            Tile((x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), [self.visible_sprites, self.collision_sprites], 'objects', tile_img)
                        elif layer.name == 'Decorations':
                            tile_img.set_colorkey('black')
                            Tile((x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), self.visible_sprites, 'objects', tile_img)
                        elif layer.name == 'Enemies':
                            monster_name = random.choice([key for key in monster_data])
                            Enemy(monster_name, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight), [self.visible_sprites, self.attackable_sprites], self.collision_sprites, self.damage_player, spritesheet_image_file = '../graphics/enemies.png')
                        elif layer.name == 'Items':
                            self.item_locations.append((x, y))
                      
        self.player = Player((1000, 1000), self.visible_sprites, self.collision_sprites, self.create_attack, self.destroy_attack, spritesheet_image_file = '../graphics/dungeon_hero_sprites.png')
        weapon_pos = random.choice(self.item_locations)
        self.item_locations.remove(weapon_pos)
        light_pos = random.choice(self.item_locations)
        self.item_locations.remove(light_pos)
        key_pos = random.choice(self.item_locations)
        self.weapon = Tile((weapon_pos[0] * self.tmx_data.tilewidth, weapon_pos[1] * self.tmx_data.tileheight), [self.visible_sprites, self.collision_sprites], 'weapon', sword_img )
        self.light = Tile((light_pos[0] * self.tmx_data.tilewidth, light_pos[1] * self.tmx_data.tileheight), [self.visible_sprites, self.collision_sprites], 'light', lamp_img )
        self.key = Tile((key_pos[0] * self.tmx_data.tilewidth, key_pos[1] * self.tmx_data.tileheight), [self.visible_sprites, self.collision_sprites], 'key', key_img )
    
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
    
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites,self.attack_sprites])
    
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)
    
    def damage_player(self, amount):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
    
    def toggle_menu(self):
        self.game_paused = not self.game_paused
        
    def end_level(self):
        self.game_exit = True
    
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.show_darkness(self.player)
        self.ui.display(self.player)
        
        if self.game_paused:
            self.ui.show_pause_menu()
        elif self.game_exit:
            self.ui.show_end_screen()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            if self.player.has_key and self.player.check_at_door():
                door_closed_sprites = [sprite for sprite in self.collision_sprites.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'door_closed']
                for sprite in door_closed_sprites:
                    sprite.remove(self.collision_sprites)
                self.visible_sprites.door_update(self.player, self.open_door_images)
                self.door_open = True

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
    
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
    
    def door_update(self, player, open_door_images):
        '''Update the door sprites when open and close to door'''
        if player.has_key:
            door_closed_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'door_closed']
            for index, sprite in enumerate(door_closed_sprites):
                sprite.image = open_door_images[index]
        