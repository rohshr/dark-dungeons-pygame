import pygame
from settings import *

class SpriteAnimationFrames:
    '''Class for storing sprite animation data'''
    def __init__(self):
        self.up = []
        self.right = []
        self.down = []
        self.left = []
        
    def __repr__(self):
        return (f"SpriteAnimationFrames(\n"
                f"  up={self.up},\n"
                f"  right={self.right},\n"
                f"  down={self.down},\n"
                f"  left={self.left}\n"
                f")")

class GameSprite(pygame.sprite.Sprite):
    """A class to represent a generic game sprite with animation support."""
    
    def __init__(self, pos, groups, spritesheet_image_file, width=SPRITE_WIDTH, height=SPRITE_HEIGHT, scale=SPRITE_SCALE, color_key = COLOR_KEY):
        super().__init__(groups)
        self.spritesheet_image_file = spritesheet_image_file
        self.spritesheet_image = pygame.image.load(spritesheet_image_file).convert_alpha()
        self.spritesheet_image.set_colorkey(color_key)
        self.width = width
        self.height = height
        self.scale = scale
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA) # set the sprite as a transparent surface
        
        # Position in the screen
        self.direction = pygame.math.Vector2()
        self.rect = self.image.get_rect(center = pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        
        self.action = ""
        self.direction_status = "down"
        self.frame_index = 0
        self.speed = ANIMATION_SPEED
        
        self.update_time = pygame.time.get_ticks()
        self.actions_list = {}
    
    def __repr__(self):
        """Return a string representation of the sprite."""
        # return f"GameSprite in {self.spritesheet_image} at ({self.x}, {self.y})"
    
    def update(self):
        pass
        # self.rect = self.image.get_rect(center = self.pos)
        # self.rect.center = self.pos
        # screen.blit(self.image, self.rect) # Draw the sprite on the screen
        # pygame.display.update()
    
    def animate(self):
        animation_timer = ANIMATION_TIMER
        if (pygame.time.get_ticks() - self.update_time > animation_timer): # condition to check current time to update the frame
            self.update_time = pygame.time.get_ticks()
            # self.frame_index = (self.frame_index + 1) % len(self.actions_list[self.action]) #getattr(self.actions_list[self.action], self.direction_status)[self.frame_index]
            self.frame_index = (self.frame_index + 1) % len(getattr(self.actions_list[self.action], self.direction_status)) #getattr(self.actions_list[self.action], self.direction_status)[self.frame_index]
            self.image = getattr(self.actions_list[self.action], self.direction_status)[self.frame_index]
