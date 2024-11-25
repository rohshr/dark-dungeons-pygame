import pygame
from settings import *
from sprite import *

class Enemy(GameSprite):
    """Class for monster sprites"""
    def __init__(self, monster_name, pos, groups, collision_sprites, spritesheet_image_file):
        
        # general setup
        super().__init__(pos, groups, collision_sprites, spritesheet_image_file)
        self.sprite_type = 'enemy'
        self.monster_name = monster_name
        
        # graphics setup
        self.action = "idle"
        self.direction_status = "down"
        self.frame_index = 0
        self.actions_list = {
            "idle": SpriteAnimationFrames(),
            "moving": SpriteAnimationFrames(),
            "attacking": SpriteAnimationFrames()
        }
        self._load_animation_frames()
        
        # Set initial image based on current action, direction, and frame index
        self.image = getattr(self.actions_list[self.action], self.direction_status)[self.frame_index]
        
        # Setting hitbox with respect to the sprite
        self.hitbox = self.rect.inflate(0, HITBOX_OFFSET['enemies'])
        self.collision_sprites = collision_sprites
        
    # Private Helper method    
    def _load_frame(self, action_frames, row, start_col, end_col):
        """Helper method to load frames for a given action and direction."""
        for col in range(start_col, end_col):
            temp_img = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            temp_img.blit(self.spritesheet_image, (0, 0), (col * SPRITE_WIDTH, row * SPRITE_HEIGHT, self.width, self.height))
            scaled_img = pygame.transform.scale(temp_img, (self.width * self.scale, self.height * self.scale))
            action_frames.append(scaled_img)

    # Private Helper method
    def _load_animation_frames(self):
        """Load frames for each action and direction efficiently."""
        directions = ["down", "left", "right", "up"]
        
        if self.monster_name == 'frog':
            actions = {
                "idle": (13, 15),
                "moving": (13, 15)
            }
        elif self.monster_name == 'skeleton':
            actions = {
                "idle": (20, 21),
                "moving": (19, 22)
            }
        elif self.monster_name == 'caveman':
            actions = {
                "idle": (16, 17),
                "moving": (15, 18)
            }
        elif self.monster_name == 'goblin':
            actions = {
                "idle": (7, 8),
                "moving": (6, 9)
            }
        
        for action, (start_col, end_col) in actions.items():
            for row, direction_status in enumerate(directions):
                action_frames = getattr(self.actions_list[action], direction_status)
                self._load_frame(action_frames, row, start_col, end_col)

    def update(self):
        self.move(self.speed)
        self.animate()