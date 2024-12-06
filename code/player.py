import pygame
from settings import *
from sprite import *

class Player(GameSprite):
    """ Class for the playable character """
    def __init__(self, pos, groups, collision_sprites, create_attack, destroy_attack, spritesheet_image_file):
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
            'has_light': False,
            'has_weapon': False,
            'has_key': False,
            'attack': 10
        }
        self.health = self.stats['health']
        self.has_light = self.stats['has_light']
        self.has_weapon = self.stats['has_weapon']
        self.has_key = self.stats['has_key']
        
        self.attacking = False
        self.attack_cooldown = 500
        self.attack_time = None
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        
        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500
  
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
        if not self.attacking:
            keys = pygame.key.get_pressed() # Checks for all pressed keys
            
            if keys[pygame.K_LSHIFT]:
                self.speed = PLAYER_SPEED * 2
            else:
                self.speed = PLAYER_SPEED
                
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
                
            elif keys[pygame.K_SPACE] and self.has_weapon:
                self.action = "attacking"
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            
            else:
                self.action = "idle"
                self.direction.x = 0
                self.direction.y = 0

    def animate(self):
        animation_timer = ANIMATION_TIMER
        frame_count = len(getattr(self.actions_list[self.action], self.direction_status))
        if (pygame.time.get_ticks() - self.update_time > animation_timer) and frame_count != 0: # condition to check current time to update the frame
            self.update_time = pygame.time.get_ticks()
            self.frame_index = (self.frame_index + 1) % frame_count
            self.image = getattr(self.actions_list[self.action], self.direction_status)[self.frame_index]
        
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
    
    def item_discovery(self):
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if sprite.sprite_type == 'weapon':
                    self.has_weapon = True
                    sprite.kill()
                elif sprite.sprite_type == 'light':
                    self.has_light = True
                    sprite.kill()
                elif sprite.sprite_type == 'key':
                    self.has_key = True
                    sprite.kill()
                    
    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        return base_damage
    
    def check_exit(self):
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.has_key and sprite.sprite_type == 'exit':
                    return True
    
    def check_at_door(self):
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.has_key and sprite.sprite_type == 'door_action_area':
                    return True

    def update(self):
        self.keypress_handler()
        self.cooldowns()
        self.animate()
        self.move(self.speed)
        self.item_discovery()