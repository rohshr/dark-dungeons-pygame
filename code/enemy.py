import pygame
from settings import *
from sprite import *

class Enemy(GameSprite):
    """Class for monster sprites"""
    def __init__(self, monster_name, pos, groups, collision_sprites, damage_player, spritesheet_image_file):
        
        # general setup
        super().__init__(pos, groups, collision_sprites, spritesheet_image_file)
        self.sprite_type = 'enemy'
        
        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        
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
        
        
        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        
        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300
        
        # import sound
        self.enemy_damage_sound = pygame.mixer.Sound('../audio/sfx/21_orc_damage_3.wav')
        self.enemy_death_sound = pygame.mixer.Sound('../audio/sfx/24_orc_death_spin.wav')
        
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
                "attacking": (13, 15),
                "moving": (13, 15)
            }
        elif self.monster_name == 'skeleton':
            actions = {
                "idle": (18, 20),
                "attacking": (18, 21),
                "moving": (18, 21)
            }
        elif self.monster_name == 'caveman':
            actions = {
                "idle": (16, 18),
                "attacking": (15, 18),
                "moving": (15, 18)
            }
        elif self.monster_name == 'goblin':
            actions = {
                "idle": (7, 9),
                "attacking": (6, 9),
                "moving": (6, 9)
            }
        
        for action, (start_col, end_col) in actions.items():
            for row, direction_status in enumerate(directions):
                action_frames = getattr(self.actions_list[action], direction_status)
                self._load_frame(action_frames, row, start_col, end_col)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)
    
    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.action != 'attacking':
                self.frame_index = 0
            self.action = 'attacking'
        elif distance <= self.notice_radius:
            self.action = 'moving'
        else:
            self.action = 'idle'

    def actions(self, player):
        if self.action == 'attacking':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage)
        elif self.action == 'moving':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()
            
    def animate(self):
        animation_timer = ANIMATION_TIMER
        frame_count = len(getattr(self.actions_list[self.action], self.direction_status))
        if (pygame.time.get_ticks() - self.update_time > animation_timer) and frame_count != 0: # condition to check current time to update the frame
            if self.action == 'attacking':
                self.can_attack = False
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
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
    
    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
            self.enemy_damage_sound.play()

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.enemy_death_sound.play()
    
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
    
    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()
    
    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)