import pygame
from settings import *
from support import *

class UI:
    def __init__(self):
        
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.font_large = pygame.font.Font(UI_FONT, UI_FONT_SIZE_LARGE).set_bold
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
        
        # UI texts
        self.texts = UI_TEXTS
        
        # text screens
        self.start_screen = pygame.image.load('../graphics/start_screen.png').convert_alpha()
        self.instructions_screen = pygame.image.load('../graphics/instructions.png').convert_alpha()
        self.pause_screen = pygame.image.load('../graphics/pause_screen.png')
        self.end_screen = pygame.image.load('../graphics/end_screen.png')
        self.death_screen = pygame.image.load('../graphics/death_screen.png')

        # Buttons
        self.start_button = Button(
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT // 2 + 64,
            width=200,
            height=50,
            text="START GAME",
            font=self.font,
            color=BUTTON_COLOR,
            hover_color=HOVER_COLOR,
            border_color=BUTTON_BORDER_COLOR,
            text_color=BUTTON_TEXT_COLOR
        )
        
        self.help_button = Button(
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT // 2 + 152,
            width=200,
            height=50,
            text="Instructions",
            font=self.font,
            color=BUTTON_COLOR,
            hover_color=HOVER_COLOR,
            border_color=TRANSPARENT_COLOR,
            text_color=TEXT_COLOR
        )
        
        self.back_button = Button(
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT // 2 + 248,
            width=200,
            height=50,
            text="Return to menu",
            font=self.font,
            color=BUTTON_COLOR,
            hover_color=HOVER_COLOR,
            border_color=TRANSPARENT_COLOR,
            text_color=TEXT_COLOR
        )
        
        self.resume_button = Button(
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT // 2 + 142,
            width=200,
            height=50,
            text="Resume",
            font=self.font,
            color=BUTTON_COLOR,
            hover_color=HOVER_COLOR,
            border_color=BUTTON_BORDER_COLOR,
            text_color=TEXT_COLOR
        )
        
        self.retry_button = Button(
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT // 2 + 64,
            width=200,
            height=50,
            text="Retry",
            font=self.font,
            color=BUTTON_COLOR,
            hover_color=HOVER_COLOR,
            border_color=BUTTON_BORDER_COLOR,
            text_color=TEXT_COLOR
        )
    
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
    
    def display_text(self, text_string, pos):
        self.display_surface.fill(UI_BG_COLOR)
        text = self.font.render(str(text_string), True, TEXT_COLOR) 
        text_rect = text.get_rect(center=pos)
        self.display_surface.blit(text, text_rect)
        pygame.display.flip()
    
    def show_start_screen(self):
        """Display the start screen."""
        self.display_surface.blit(self.start_screen, (0, 0))
        
    def show_instructions_screen(self):
        """Display the instructions screen."""
        self.display_surface.blit(self.instructions_screen, (0, 0))
        
    def show_pause_menu(self):
        """Display the pause screen."""
        self.display_surface.blit(self.pause_screen, (0, 0))
    
    def show_death_screen(self):
        """Display the death screen."""
        self.display_surface.blit(self.death_screen, (0, 0))
        
    def show_end_screen(self):
        """Display the ending screen."""
        self.display_surface.blit(self.end_screen, (0, 0))
        
  
    def display(self, player):
        self.show_hp(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_inventory()
        self.update_inventory('weapon', player.has_weapon)
        self.update_inventory('light', player.has_light)
        self.update_inventory('key', player.has_key)

class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, border_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.border_color = border_color
        self.text_color = text_color
        self.is_hovered = False

        # Render the text
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        # Change color if hovered
        button_color = self.hover_color if self.is_hovered else self.color

        # Draw button border
        pygame.draw.rect(screen, self.border_color, self.rect)

        # Draw inner button
        inner_rect = self.rect.inflate(-4, -4)  # Create a smaller inner rectangle for the button face
        pygame.draw.rect(screen, button_color, inner_rect)

        # Draw text
        screen.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        """Handle events like mouse hover and clicks."""
        if event.type == pygame.MOUSEMOTION:
            # Check if mouse is over the button
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1:  # Left mouse button
                return True  # Button clicked
        return False
