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
DARK_BLUE = (0, 0, 128)
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
RATE = 3 
RIGHT = (RATE, 0)
LEFT = (-RATE, 0)
UP = (0, -RATE)
DOWN = (0, RATE) 

# Tower upgrades 
# added upgrade_list
tower_max_level = 1 
upgrade_list = [GREEN, CYAN]
tower_damage = {GREEN : 0.5, CYAN : 1}
tower_cost = {GREEN : 10, CYAN : 20}
tower_size = {GREEN : (20, 20), CYAN : (30, 30)}
tower_range = {GREEN : 160, CYAN : 170}
space_between = 40