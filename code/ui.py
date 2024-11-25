import pygame
from settings import *
from support import *

class UI:
    def __init__(self):
        
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.screen_width = self.display_surface.get_size()[0]
        self.screen_height = self.display_surface.get_size()[1]
        
        # bar setup
        self.health_bar_rect = pygame.Rect(48, 15, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.heart_icon = pygame.image.load(HEART_ICON).convert_alpha()
        self.heart_icon_rect = pygame.Rect(10, 10, 32, 32)
        
        # invetory setup
        self.light_images = get_image_surfaces(inventory_data['light'])
        self.light_rect = pygame.Rect(self.screen_width - 72, 10, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        self.weapon_images = get_image_surfaces(inventory_data['weapon'])
        self.weapon_rect = pygame.Rect(self.screen_width - 136, 10, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        self.key_images = get_image_surfaces(inventory_data['key'])
        self.key_rect = pygame.Rect(self.screen_width - 200, 10, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
    
    def show_hp(self, current, max_amount, bg_rect, color):
        # draw heart icon
        self.display_surface.blit(self.heart_icon, self.heart_icon_rect)
        
        # draw bg 
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect, 3)
    
    def show_inventory(self):
        # weapon
        self.display_surface.blit(self.weapon_images[0], self.weapon_rect)
        
        # light
        self.display_surface.blit(self.light_images[0], self.light_rect)

        # key
        self.display_surface.blit(self.key_images[0], self.key_rect)
        
    def update_inventory(self, item, state):
        image_index = (1 if state else 0)
        if item == 'weapon':
            self.display_surface.blit(self.weapon_images[image_index], self.weapon_rect)
        elif item == 'light':
            self.display_surface.blit(self.light_images[image_index], self.light_rect)
        if item == 'key':
            self.display_surface.blit(self.key_images[image_index], self.key_rect)
            
  
    def display(self, player):
        self.show_hp(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_inventory()
        self.update_inventory('weapon', True)
        self.update_inventory('light', True)
        self.update_inventory('key', True)