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
RATE = 3
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


rifle_stats = {
	"damage" : {GREEN : 25, CYAN : 30, BLUE : 35, DARK_BLUE : 40, YELLOW : 45, ORANGE : 50,
					MAGENTA : 55, WHITE : 60},

	"cost" : {GREEN : 5, CYAN : 10, BLUE : 15, DARK_BLUE : 20, YELLOW : 30, ORANGE : 40,
					MAGENTA : 60, WHITE : 80},

	"inflation" : {GREEN : (0, 0), CYAN : (0, 0), BLUE : (10, 10), DARK_BLUE : (0, 0), 
				  YELLOW : (5, 5), ORANGE : (0, 0), MAGENTA : (5, 5), WHITE : (5, 5)},

	"range" : {GREEN : 180, CYAN : 190, BLUE : 200, DARK_BLUE : 210, YELLOW : 220, ORANGE : 230,
					MAGENTA : 240, WHITE : 250},

	"reload": 30,


	"shell_speed": 20
}

sniper_stats = {
	"damage" : {GREEN : 80, CYAN : 90, BLUE : 100, DARK_BLUE : 120, YELLOW : 140, ORANGE : 160,
					MAGENTA : 180, WHITE : 200},

	"cost" : {GREEN : 50, CYAN : 100, BLUE : 150, DARK_BLUE : 200, YELLOW : 300, ORANGE : 400,
					MAGENTA : 600, WHITE : 800},

	"inflation" : {GREEN : (0, 0), CYAN : (0, 0), BLUE : (10, 10), DARK_BLUE : (0, 0), 
				  YELLOW : (5, 5), ORANGE : (0, 0), MAGENTA : (5, 5), WHITE : (5, 5)},

	"range" : {GREEN : 240, CYAN : 260, BLUE : 280, DARK_BLUE : 300, YELLOW : 310, ORANGE : 320,
					MAGENTA : 330, WHITE : 340},

	"reload": 90,


	"shell_speed": 30

}

machine_gun_stats = {
	"damage" : {GREEN : 5, CYAN : 10, BLUE : 15, DARK_BLUE : 20, YELLOW : 25, ORANGE : 30,
					MAGENTA : 35, WHITE : 40},

	"cost" : {GREEN : 50, CYAN : 100, BLUE : 150, DARK_BLUE : 200, YELLOW : 300, ORANGE : 400,
					MAGENTA : 600, WHITE : 800},

	"inflation" : {GREEN : (0, 0), CYAN : (0, 0), BLUE : (10, 10), DARK_BLUE : (0, 0), 
				  YELLOW : (5, 5), ORANGE : (0, 0), MAGENTA : (5, 5), WHITE : (5, 5)},

	"range" : {GREEN : 160, CYAN : 170, BLUE : 180, DARK_BLUE : 190, YELLOW : 200, ORANGE : 210,
					MAGENTA : 220, WHITE : 230},

	"reload": 4,
	

	"shell_speed": 15

}


tower_classes = {"rifle": rifle_stats, "sniper": sniper_stats, "machine_gun": machine_gun_stats, "heavy": 4}

tower_damage = {GREEN : 25, CYAN : 30, BLUE : 35, DARK_BLUE : 40, YELLOW : 45, ORANGE : 50,
				MAGENTA : 55, WHITE : 60}

tower_cost = {GREEN : 5, CYAN : 10, BLUE : 15, DARK_BLUE : 20, YELLOW : 30, ORANGE : 40,
				MAGENTA : 60, WHITE : 80}

tower_inflation = {GREEN : (0, 0), CYAN : (0, 0), BLUE : (10, 10), DARK_BLUE : (0, 0), 
			  YELLOW : (5, 5), ORANGE : (0, 0), MAGENTA : (5, 5), WHITE : (5, 5)}

tower_range = {GREEN : 180, CYAN : 190, BLUE : 200, DARK_BLUE : 210, YELLOW : 220, ORANGE : 230,
				MAGENTA : 240, WHITE : 250}

# enemy stuff 
counter = 0
spawn_time = 50
enemy_size = (30, 30)
enemy_start = (10, HEIGHT / 2)
enemy_speed = RIGHT
enemy_initial_hp = 100 
enemy_max_hp = 100