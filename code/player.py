import pygame
from settings import *
from sprite import *

class Player(GameSprite):
    """ Class for the playable character """
    def __init__(self, pos, groups, collision_sprites, spritesheet_image_file):
        super().__init__(pos, groups, spritesheet_image_file)
        # self.position = pos
        self.spritesheet_rows = 8
        self.spritesheet_cols = 12
        self.action = "idle"
        self.direction_status = "down"
        self.frame_index = 0
        self.actions_list = {
            "idle": SpriteAnimationFrames(),
            "walking": SpriteAnimationFrames(),
            "digging": SpriteAnimationFrames()
        }
        self._load_animation_frames()
        
        # Set initial image based on current action, direction, and frame index
        self.image = getattr(self.actions_list[self.action], self.direction_status)[self.frame_index]
        
        # Setting hitbox with respect to the sprite
        self.hitbox = self.rect.inflate(0, 0)
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
        actions = {
            "idle": (3, 6),    # Columns 3-5
            "walking": (0, 4), # Columns 0-3
            "digging": (15, 18)  # Columns 15-17
        }
        
        for action, (start_col, end_col) in actions.items():
            for row, direction_status in enumerate(directions):
                action_frames = getattr(self.actions_list[action], direction_status)
                self._load_frame(action_frames, row, start_col, end_col)
    
    def keypress_handler(self):
        """Method to handle key presses for player actions."""
        keys = pygame.key.get_pressed() # Checks for all pressed keys
        # Update movement vector based on key input
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
            self.action = "digging"
        
        else:
            self.action = "idle"
            self.direction.x = 0
            self.direction.y = 0
            # self.direction_status = (0, 0)
    
    # def move(self):
    #     '''Function to move the character'''
    #     # Normalize the movement vector to prevent faster diagonal movement
    #     if self.direction.magnitude() > 0:
    #         self.direction = self.direction.normalize()

    #     # Update the player's position
    #     # horizontal movement
    #     self.hitbox.x += self.direction.x * self.speed
    #     self.collision('horizontal')
        
    #     # vertical movement
    #     self.hitbox.y += self.direction.y * self.speed
    #     self.collision('vertical')
    #     # self.rect.center = self.position
        
    #     self.rect.center = self.hitbox.center
        
    #     pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), self.hitbox, 2)
        
        
        # Ensure the player stays within screen boundaries
        # self.rect.x = max(0, min(SCREEN_WIDTH - self.width, self.pos.x))
        # self.rect.y = max(0, min(SCREEN_HEIGHT - self.height, self.pos.y))

    # def collision(self, axis):
    #     if axis == 'horizontal':
    #         for sprite in self.collision_sprites:
    #             if sprite.hitbox.colliderect(self.hitbox): # check the rect of collision object with the rect of player
    #                 pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), sprite.hitbox, 2)
    #                 if self.direction.x > 0: # check right movement
    #                     self.hitbox.right = sprite.hitbox.left # collision for right side of the player rect to the left side of the collider rect
    #                 elif self.direction.x < 0:# check left movement
    #                     self.hitbox.left = sprite.hitbox.right # when moving left
        
    #     if axis == 'vertical':
    #         for sprite in self.collision_sprites:
    #             if sprite.hitbox.colliderect(self.hitbox):
    #                 if self.direction.y < 0: # check up movement
    #                     self.hitbox.top = sprite.hitbox.bottom 
    #                 elif self.direction.y > 0: # check down movement
    #                     self.hitbox.bottom = sprite.hitbox.top 

    def update(self):
        # self.draw(pygame.display.get_surface())
        self.keypress_handler()
        self.move(ANIMATION_SPEED)
        self.animate()
        
  
# class Player(pygame.sprite.Sprite):
# 	def __init__(self, pos, groups):
# 		super().__init__(groups)
# 		self.image = pygame.image.load('../graphics/test/star.png')
# 		self.rect = self.image.get_rect(topleft = pos)