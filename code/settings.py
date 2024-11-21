from pygame.math import Vector2

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
HITBOX_OFFSET = {
	'player': 0,
	'object': 0,
	'walls': 0,
    'floor': 0,
	'invisible': 0}

SPRITE_WIDTH = 24
SPRITE_HEIGHT = 32
TILE_SIZE = 16  # Size of each grid cell

SPRITE_SCALE = 2
COLOR_KEY = (255, 0, 255) # Not black because the sprites have black outline
ANIMATION_TIMER = 200
ANIMATION_SPEED = 4