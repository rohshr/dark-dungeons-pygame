import pygame
from settings import *
from sprite import *

class Player(GameSprite):
    """ Class for the playable character """
    def __init__(self, pos, groups, collision_sprites, spritesheet_image_file):
        super().__init__(pos, groups, collision_sprites, spritesheet_image_file)
        # self.position = pos
        self.action = "idle"
        self.direction_status = "down"
        self.frame_index = 0
        self.actions_list = {
            "idle": SpriteAnimationFrames(),
            "walking": SpriteAnimationFrames(),
            "digging": SpriteAnimationFrames(),
            "attacking": SpriteAnimationFrames()
        }
        self._load_animation_frames()
        
        # Set initial image based on current action, direction, and frame index
        self.image = getattr(self.actions_list[self.action], self.direction_status)[self.frame_index]
        
        # Setting hitbox with respect to the sprite
        self.hitbox = self.rect.inflate(0, HITBOX_OFFSET['player'])
        self.collision_sprites = collision_sprites
        
        # stats
        self.stats = {
            'health': 100,
            'has_light': True,
            'has_weapon': False,
            'has_key': False
        }
        self.health = self.stats['health']
        self.has_light = self.stats['has_light']
        self.has_weapon = self.stats['has_weapon']
        self.has_key = self.stats['has_key']

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
        actions = {
            "idle": (3, 6),    # Columns 3-5
            "walking": (0, 4), # Columns 0-3
            "digging": (15, 18),  # Columns 15-17
            "attacking": (18, 21)
        }
        
        for action, (start_col, end_col) in actions.items():
            for row, direction_status in enumerate(directions):
                action_frames = getattr(self.actions_list[action], direction_status)
                self._load_frame(action_frames, row, start_col, end_col)
    
    def keypress_handler(self):
        """Method to handle key presses for player actions."""
        keys = pygame.key.get_pressed() # Checks for all pressed keys
        # Update movement vector based on key input
        if keys[pygame.K_LSHIFT]:
            self.speed = ANIMATION_SPEED * 2
        else:
            self.speed = ANIMATION_SPEED
            
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.action = "walking"
            self.direction.y = -1
            self.direction_status = "up"
    
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.action = "walking"
            self.direction.y = 1
            self.direction_status = "down"
            
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.action = "walking"
            self.direction.x = -1
            self.direction_status = "left"

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.action = "walking"
            self.direction.x = 1
            self.direction_status = "right"
             
        elif keys[pygame.K_SPACE]:
            self.action = "attacking"
        
        else:
            self.action = "idle"
            self.direction.x = 0
            self.direction.y = 0

    def update(self):
        self.keypress_handler()
        self.move(self.speed)
        self.animate()