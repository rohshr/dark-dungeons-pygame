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
    
    def create_map(self):
        self.item_locations = []
        self.door_location = []
        self.open_door_images = []

        # Load common sprites
        key_img = pygame.image.load('../graphics/key.png').convert_alpha()
        sword_img = pygame.image.load('../graphics/sword.png').convert_alpha()
        lamp_img = pygame.image.load('../graphics/lamp.png').convert_alpha()
        
        def set_black_colorkey(img):
            """Utility function to set black as colorkey for images."""
            if img:
                img = img.convert_alpha()
                img.set_colorkey('black')
            return img

        layer_actions = {
            'FloorBlocks': lambda x, y, img: Tile((x, y), self.collision_sprites, 'invisible'),
            'Walls': lambda x, y, img: Tile((x, y), [self.visible_sprites, self.collision_sprites], 'walls', img),
            'DoorClosed': lambda x, y, img: Tile((x, y), [self.visible_sprites, self.collision_sprites], 'door_closed', img),
            'DoorActionArea': lambda x, y, img: Tile((x, y), self.collision_sprites, 'door_action_area'),
            'DoorOpen': self.handle_door_open_layer,
            'Exit': lambda x, y, img: Tile((x, y), self.collision_sprites, 'exit'),
            'InnerWalls': lambda x, y, img: Tile((x, y), [self.visible_sprites, self.collision_sprites], 'inner_walls', set_black_colorkey(img)),
            'DungeonEnvironment': lambda x, y, img: Tile((x, y), [self.visible_sprites, self.collision_sprites], 'objects', set_black_colorkey(img)),
            'Decorations': lambda x, y, img: Tile((x, y), self.visible_sprites, 'objects', set_black_colorkey(img)),
            'Enemies': self.handle_enemies_layer,
            'Items': self.handle_items_layer
        }

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_img = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile_img:
                        tile_img = tile_img.convert_alpha()
                        tile_img.set_colorkey(COLOR_KEY)
                        action = layer_actions.get(layer.name)
                        if action:
                            action(x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight, tile_img)

        # Set up random items (weapon, light, key)
        weapon_pos = random.choice(self.item_locations)
        self.item_locations.remove(weapon_pos)
        light_pos = random.choice(self.item_locations)
        self.item_locations.remove(light_pos)
        key_pos = random.choice(self.item_locations)

        self.weapon = Tile((weapon_pos[0] * self.tmx_data.tilewidth, weapon_pos[1] * self.tmx_data.tileheight),
                        [self.visible_sprites, self.collision_sprites], 'weapon', sword_img)
        self.light = Tile((light_pos[0] * self.tmx_data.tilewidth, light_pos[1] * self.tmx_data.tileheight),
                        [self.visible_sprites, self.collision_sprites], 'light', lamp_img)
        self.key = Tile((key_pos[0] * self.tmx_data.tilewidth, key_pos[1] * self.tmx_data.tileheight),
                        [self.visible_sprites, self.collision_sprites], 'key', key_img)
        
        # Set up player
        self.handle_player_start_layer(1000, 1000)
        

    def handle_player_start_layer(self, x, y):
        """Handle player start position."""
        self.player = Player(
            (x, y), 
            self.visible_sprites, 
            self.collision_sprites, 
            self.create_attack, 
            self.destroy_attack, 
            spritesheet_image_file='../graphics/dungeon_hero_sprites.png'
        )
    
    def handle_door_open_layer(self, x, y, img):
        img.set_colorkey('black')
        self.door_location.append((x, y))
        self.open_door_images.append(img)

    def handle_enemies_layer(self, x, y, _):
        monster_name = random.choice(list(monster_data.keys()))
        Enemy(
            monster_name,
            (x, y),
            [self.visible_sprites, self.attackable_sprites],
            self.collision_sprites,
            self.damage_player,
            spritesheet_image_file='../graphics/enemies.png'
        )

    def handle_items_layer(self, x, y, _):
        self.item_locations.append((x // self.tmx_data.tilewidth, y // self.tmx_data.tileheight))
    
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
        # self.show_darkness(self.player)
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
        
        # darkness overlay
        self.darkness_overlay = [self.get_darkness_overlay(100), self.get_darkness_overlay(300)]
        
        
    def custom_draw(self, player):
        
        # getting offset from the player
        self.offset.x = player.rect.centerx - self.screen_width // 2 + player.rect.width // 2 # offset to the exact center of the player
        self.offset.y = player.rect.centery - self.screen_height // 2 + player.rect.height // 2

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
                    
        if player.has_light:
            self.display_surface.blit(self.darkness_overlay[1], (0, 0))
        else:
            self.display_surface.blit(self.darkness_overlay[0], (0, 0))
            
            
    def enemy_update(self, player):
        # enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        # for enemy in enemy_sprites:
        #     enemy.enemy_update(player)
        activation_radius = 500  # Distance to activate enemies
        enemy_sprites = [
            sprite for sprite in self.sprites() 
            if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy'
        ]
        for enemy in enemy_sprites:
            if abs(player.rect.centerx - enemy.rect.centerx) < activation_radius and \
            abs(player.rect.centery - enemy.rect.centery) < activation_radius:
                enemy.enemy_update(player)
    
    def door_update(self, player, open_door_images):
        '''Update the door sprites when open and close to door'''
        if player.has_key:
            door_closed_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'door_closed']
            for index, sprite in enumerate(door_closed_sprites):
                sprite.image = open_door_images[index]
                
    def get_darkness_overlay(self, radius):
        
        # darkness setup
        darkness_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        darkness_overlay = pygame.draw.rect(darkness_surface, 'white', (0, 0, self.screen_width, self.screen_height))
        
        # circle of vision in the center
        vision_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        circle_x, circle_y = self.screen_width // 2, self.screen_height // 2
        
        vision_overlay = pygame.draw.circle(vision_surface, 'white', (circle_x, circle_y), radius)
        
        mask_darkness = pygame.mask.from_surface(darkness_surface)
        mask_vision = pygame.mask.from_surface(vision_surface)
        mask_vision.invert()
        subtract_masks = mask_darkness.overlap_mask(mask_vision, (0, 0))
        
        subtract_shapes = subtract_masks.to_surface(darkness_surface, setcolor = 'black', unsetcolor = (0, 0, 0, 0))
        
        return subtract_shapes
        