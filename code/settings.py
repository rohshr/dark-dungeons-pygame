from pygame.math import Vector2

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
HITBOX_OFFSET = {
    'player': 0,
    'objects': 10,
    'walls': -15,
    'inner_walls': -15,
    'floor': 0,
    'invisible': 0,
    'enemies': 0
    }

SPRITE_WIDTH = 24
SPRITE_HEIGHT = 32
TILE_SIZE = 16  # Size of each grid cell

SPRITE_SCALE = 2
COLOR_KEY = (255, 0, 255) # Not black because the sprites have black outline
ANIMATION_TIMER = 200
ANIMATION_SPEED = 4

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 64
UI_FONT = '../graphics/font/PixeloidSans-mLxMm.ttf'
UI_FONT_SIZE = 18

# Color Pallette
TEXT_COLOR = '#EFEFEF'
UI_BG_COLOR = '#333333'
UI_BORDER_COLOR = '#121212'

HEALTH_COLOR = 'red'
HEART_ICON = '../graphics/ui/heart.png'
UI_BORDER_COLOR_ACTIVE = 'gold'
DARKNESS_COLOR = 'black'
ENEMY_FOOTSTEP_COLOR = '#F42718'

# invetory setup
inventory_data = {
    'light': ['../graphics/ui/light_inactive.png', '../graphics/ui/light_active.png'],
    'key': ['../graphics/ui/key_inactive.png', '../graphics/ui/key_active.png'],
    'weapon': ['../graphics/ui/weapon_inactive.png', '../graphics/ui/weapon_active.png']
}

monster_data = {
	'frog': {'health': 50,'exp':100,'damage':5, 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'skeleton': {'health': 100,'exp':250,'damage':40, 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'caveman': {'health': 70,'exp':110,'damage':8, 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'goblin': {'health': 90,'exp':120,'damage':6, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}
 }