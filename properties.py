import pygame, sys
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
GRAY = (100, 100, 100)

# Mixer is for sounds
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# Sounds
rifle_gun = pygame.mixer.Sound(file="sounds/rifle_gun.wav")
sniper_gun = pygame.mixer.Sound(file="sounds/sniper_gun.wav")
machine_gun = pygame.mixer.Sound(file="sounds/machine_gun.wav")
player_gun = pygame.mixer.Sound(file="sounds/player_gun.wav")
heavy_gun = pygame.mixer.Sound(file="sounds/heavy_gun.wav")

explode_sound = pygame.mixer.Sound(file="sounds/explode_sound.wav")

tower_sounds = {
    "rifle" : rifle_gun,
    "sniper" : sniper_gun,
    "machine_gun" : machine_gun,
    "heavy" : heavy_gun
}

# Timing constants 
FRAME_RATE = 30
TICK_SPEED = 300 

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
space_between = 40
UPGRADE_DELAY = 300
INITIAL_SIZE = (20, 20)
upgrade_list = [GREEN, CYAN, BLUE, DARK_BLUE, YELLOW, ORANGE, MAGENTA, WHITE]
