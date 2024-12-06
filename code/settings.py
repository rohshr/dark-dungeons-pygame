from pygame.math import Vector2

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 30
HITBOX_OFFSET = {
    'player': 0,
    'objects': 10,
    'walls': -15,
    'inner_walls': -15,
    'door_closed': 0,
    'door_open': 0,
    'door_action_area': 0,
    'exit': -10,
    'floor': 0,
    'invisible': 0,
    'weapon': 0,
    'light': 0,
    'key': 0,
    'enemies': -10
    }

SPRITE_WIDTH = 24
SPRITE_HEIGHT = 32
TILE_SIZE = 16  # Size of each grid cell

SPRITE_SCALE = 2
COLOR_KEY = (255, 0, 255) # Not black because the sprites have black outline
ANIMATION_TIMER = 200
ANIMATION_SPEED = 2

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 64
UI_FONT = '../graphics/font/PixeloidSans-mLxMm.ttf'
UI_FONT_SIZE = 18
UI_FONT_SIZE_LARGE = 24
UI_FONT_SIZE_XL = 64

# Color Pallette
TEXT_COLOR = '#EFEFEF'
UI_BG_COLOR = '#020202'
UI_BORDER_COLOR = '#121212'
BUTTON_COLOR = (50, 50, 50)  # Dark gray
HOVER_COLOR = (100, 100, 100)  # Light gray for hover effect
BUTTON_BORDER_COLOR = (150, 75, 0)  # Brownish
BUTTON_TEXT_COLOR = (200, 200, 200)  # Light gray text
TRANSPARENT_COLOR = (255, 255, 255, 0)

HEALTH_COLOR = 'red'
HEART_ICON = '../graphics/ui/heart.png'
UI_BORDER_COLOR_ACTIVE = 'gold'
DARKNESS_COLOR = 'black'
ENEMY_FOOTSTEP_COLOR = '#F42718'
PLAYER_SPEED = 5

# music
MAIN_MENU_MUSIC = '../audio/music/Goblins_Den_(Regular).wav'
IN_GAME_MUSIC = '../audio/music/Goblins_Dance_(Battle).wav'

# invetory setup
inventory_data = {
    'light': ['../graphics/ui/light_inactive.png', '../graphics/ui/light_active.png'],
    'key': ['../graphics/ui/key_inactive.png', '../graphics/ui/key_active.png'],
    'weapon': ['../graphics/ui/weapon_inactive.png', '../graphics/ui/weapon_active.png']
}

monster_data = {
	'frog': {'health': 100,'exp':100,'damage': -2, 'speed': 4, 'resistance': 40, 'attack_radius': 20, 'notice_radius': 300},
	'skeleton': {'health': 200,'exp':250,'damage':5, 'speed': 3, 'resistance': 15, 'attack_radius': 20, 'notice_radius': 400},
	'caveman': {'health': 200,'exp':110,'damage':2, 'speed': 2, 'resistance': 10, 'attack_radius': 20, 'notice_radius': 200},
	'goblin': {'health': 100,'exp':120,'damage':1, 'speed': 2, 'resistance': 20, 'attack_radius': 20, 'notice_radius': 200}
 }

UI_TEXTS = {
    'pause': "Game Paused",
    'game_title': "Dark Dungeon",
    'instructions': "Escape the dark and treacherous dungeon alive.",
    'tasks': "The lamp helps you see further.\nSword helps you fight off the terrors lurking within the dungeon.\nYou will need to find the key to open the door. But where is the door?",
    'escape': "Congratulations! You escaped the horrors of the dungeon.",
    'death': "You died"
}