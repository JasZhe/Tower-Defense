# Game properties can be changed/added here

# Colours
RED = (255, 51, 51)
ORANGE = (255, 153, 51)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (30, 144, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MAGENTA = (255, 0, 255)
DARK_BLUE = (0, 30, 205)
CYAN = (0, 255, 255)

# Timing constants 
FRAME_RATE = 30
TICK_SPEED = 300 

# Window size properties
WIDTH = 1024
HEIGHT = 768
SIZE = (WIDTH, HEIGHT) 


# Bullet properties
SHOT_DELAY = 250
SHOT_DMG = 20
SHOT_WIDTH = 5
SHOT_HEIGHT = 20

# Direction constants
RATE = 2
RIGHT = (RATE, 0)
LEFT = (-RATE, 0)
UP = (0, -RATE)
DOWN = (0, RATE) 

# Tower upgrades 
# added upgrade_list
tower_max_level = 7
space_between = 70
UPGRADE_DELAY = 300
INITIAL_SIZE = (20, 20)
upgrade_list = [GREEN, CYAN, BLUE, DARK_BLUE, YELLOW, ORANGE, MAGENTA, WHITE]

tower_damage = {GREEN : 5, CYAN : 0.75, BLUE : 1, DARK_BLUE : 1.25, YELLOW : 1.5, ORANGE : 1.75,
				MAGENTA : 2, WHITE : 2.25}

tower_cost = {GREEN : 5, CYAN : 10, BLUE : 15, DARK_BLUE : 20, YELLOW : 30, ORANGE : 40,
				MAGENTA : 60, WHITE : 80}

tower_inflation = {GREEN : (0, 0), CYAN : (0, 0), BLUE : (10, 10), DARK_BLUE : (0, 0), 
			  YELLOW : (5, 5), ORANGE : (0, 0), MAGENTA : (5, 5), WHITE : (5, 5)}

tower_range = {GREEN : 360, CYAN : 170, BLUE : 180, DARK_BLUE : 185, YELLOW : 190, ORANGE : 195,
				MAGENTA : 200, WHITE : 210}

# enemy stuff 
counter = 0
spawn_time = 50
enemy_size = (30, 30)
enemy_start = (10, HEIGHT / 2)
enemy_speed = RIGHT
enemy_initial_hp = 100 
enemy_max_hp = 100