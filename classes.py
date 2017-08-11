import pygame, sys
from functions import *
from properties import * 

# A module of all classes in the game

class Player(object): 
    def __init__(self, body, colour, screen_width, screen_height, x, y, direction = "U", gun_size = 5, gun_colour = (255,255,0)): 
        self.body = body
        self.colour = colour
        self.screen_width = screen_width
        self.screen_height = screen_height  
        self.horizontal_speed = x
        self.vertical_speed = y
        self.direction = direction
        self.gun_size = gun_size
        self.gun_colour = gun_colour

    def update(self, x = 0, y = 0):
        # Make sure the player can't leave the screen. 
        if ((self.body.right >= self.screen_width and x > 0) or 
            (self.body.x <= 0 and x < 0)):

            self.body.move_ip(0, y)
        elif ((self.body.bottom >= self.screen_height and y > 0) or 
            (self.body.y <= 0 and y < 0)):

            self.body.move_ip(x, 0)
        else:
            self.body.move_ip(x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.body)

        if self.direction == "U":
            pygame.draw.rect(screen, self.gun_colour, 
                pygame.Rect(coord_add(self.body.topleft, ((self.body.width - self.gun_size)/2,  -self.gun_size)), 
                    (self.gun_size, self.gun_size)))
        elif self.direction == "D":
            pygame.draw.rect(screen, self.gun_colour, 
            pygame.Rect(coord_add(self.body.bottomleft, ((self.body.width - self.gun_size)/2,  0)), 
                (self.gun_size, self.gun_size)))
        elif self.direction == "L":
            pygame.draw.rect(screen, self.gun_colour, 
            pygame.Rect(coord_add(self.body.topleft, (-self.gun_size/2,  (self.body.height - self.gun_size)/2)), 
                (self.gun_size, self.gun_size)))
        else:
            pygame.draw.rect(screen, self.gun_colour, 
            pygame.Rect(coord_add(self.body.topright, (0,  (self.body.height - self.gun_size)/2)), 
                (self.gun_size, self.gun_size)))

class Enemy(object):
        # Add health 
        def __init__(self, body, colour, velocity, screen_width, screen_height, hp, max_hp = 100):

            self.body = body 
            self.velocity = velocity # Tuple (v_x, v_y)
            self.colour = colour 
            self.screen_width = screen_width
            self.screen_height = screen_height
            self.hp = hp
            self.max_hp = max_hp


        def update(self):
            self.body.move_ip(self.velocity)

        # Return true if the enemy has left the screen or destroyed
        def check_destroy(self, percent_margin = 0.2):
            if self.hp <= 0 \
            or self.body.top > self.screen_height * (1 + percent_margin) \
            or self.body.bottom < 0 - self.screen_height * percent_margin \
            or self.body.left > self.screen_width * (1 + percent_margin) \
            or self.body.right < 0 - self.screen_width * percent_margin:
                return True
            else:
                return False

        # get_direction()
        # returns the direction that the enemy is going
        # Void -> One of ['U', 'D', 'L', 'R']
        def get_direction(self):
            if self.velocity[0] == 0:
                if self.velocity[1] > 0:
                    return 'D'
                else:
                    return 'U'
            elif self.velocity[0] > 0:
                return 'R'
            else:
                return 'L'
        # turn
        # Changes the direction that the enemy is going
        # One of ['U', 'D', 'L', 'R'] -> Void
        def turn(self, direction):
            speed = max(abs(self.velocity[0]), abs(self.velocity[1]))
            if direction == 'U':
                self.velocity = (0, -speed)
            elif direction == 'D':
                self.velocity = (0, speed)
            elif direction == 'L':
                self.velocity = (-speed, 0)
            elif direction == 'R':
                self.velocity = (speed, 0)


class Bullet(object):
    def __init__(self, speed, pos, colour, screen_height, screen_width, width = 5, height = 20, damage = 10):
        self.speed = speed
        # Inital position of the bullet ie. where the player made the shot 
        self.body = pygame.Rect(pos, (width, height))
        self.colour = colour 
        self.screen_height = screen_height 
        self.screen_width = screen_width
        self.damage = damage

    def update(self):
        self.body.move_ip(self.speed) 

    # Return true if the bullet leaves the screen
    # percent_margin is the the margin buffer outsize the view before it's destroyed
    def check_destroy(self, percent_margin = 0.2):
        if self.body.top > self.screen_height * (1 + percent_margin) \
        or self.body.bottom < 0 - self.screen_height * percent_margin \
        or self.body.left > self.screen_width * (1 + percent_margin) \
        or self.body.right < 0 - self.screen_width * percent_margin:
            return True
        else:
            return False

class Tower(object):
    def __init__(self, pos, tower_class = "rifle"):
        # moved space_between to properties
        # shellSpeed should be >= 10, anything smaller will create rounding inaccuracies
        self.pos = pos 
        self.level = 0
        self.tower_class = tower_class      
        self.type =  upgrade_list[self.level] # Each tower type will have a different colour  
        self.max_range = tower_classes[self.tower_class]["range"][self.type]  # Range is the radius 
        self.damage = tower_classes[self.tower_class]["damage"][self.type]
        self.cost = tower_classes[self.tower_class]["damage"][self.type]
        self.body = pygame.Rect(self.pos, INITIAL_SIZE)
        self.reload = tower_classes[self.tower_class]["reload"]
        self.shell_speed = tower_classes[self.tower_class]["shell_speed"]
        self.time = 0


    def upgrade(self):
        self.level = self.level + 1         
        self.type =  upgrade_list[self.level] # Each tower type will have a different colour  
        self.max_range = tower_classes[self.tower_class]["range"][self.type]  # Range is the radius 
        self.damage = tower_classes[self.tower_class]["damage"][self.type]
        self.cost = tower_classes[self.tower_class]["damage"][self.type]
        self.body.inflate_ip(tower_classes[self.tower_class]["inflation"][self.type])

    # shoots at enemy when time is right
    def canShoot(self):
        if self.time % self.reload == 0:
            self.time = 0
            return True
        else:
            return False

    # Calculates damage rate (Damage Per Frame)
    def dpm(self):
        return self.damage / self.reload

# Class for the game map
# Constructor: listOf(listOf(Int))
# Requires: Each list must be the same length
class Map:
    # Generates game map based off of the map file
    def __init__(self, map_file):
        previous_corner = None
        line_number = 1
        self.corners = []
        with open(map_file, 'r') as file:
            for line in file:
                if line_number == 1:
                    self.rows = int(line.split(':')[1])
                elif line_number == 2:
                    self.cols = int(line.split(':')[1])
                    grid = [' '] * self.rows
                    for i in range(0, self.rows):
                        grid[i] = [' '] * self.cols
                        self.grid = grid
                elif line_number == 3:
                    self.grid_size = int(line.split(':')[1])
                else:
                    coords = line.strip().split(',')
                    self.corners.append((int(coords[0]), int(coords[1])))
                    self.grid[int(coords[0])][int(coords[1])] = 'P'
                line_number = line_number + 1
            file.close()

        corner_len = len(self.corners)
        for i in range(0, corner_len):
            if i + 1 < corner_len:
                if self.corners[i][0] == self.corners[i + 1][0]:
                    lower = min(self.corners[i][1], self.corners[i + 1][1])
                    higher = max(self.corners[i][1], self.corners[i + 1][1])
                    for k in range (lower, higher):
                        self.grid[self.corners[i][0]][k] = 'P'

                elif self.corners[i][1] == self.corners[i + 1][1]:
                    lower = min(self.corners[i][0], self.corners[i + 1][0])
                    higher = max(self.corners[i][0], self.corners[i + 1][0])
                    for k in range (lower, higher):
                        self.grid[k][self.corners[i][1]] = 'P'

    def save_map(self, file_name = 'map_view.txt'):
        with open(file_name, 'w') as file:
            for row in self.grid:
                file.write(str(row) + '\n')
            file.close()

    # Finds the length of the map
    def row_length(self):
        return len(self.grid[0])

    # Find the height of the map
    def col_length(self):
        return len(self.grid)

    # Checks if a set of index is valid in the map
    def check_valid(self, row = False, col = False):
        if row == False and col == False:
            row_length = self.row_length()
            for row in self.grid:
                if len(row) != row_length:
                    return False
            return True

        elif row >= self.col_length() or col >= self.row_length():
            print("Invalid parameters!")
            return False
        else:
            return True

    # Converts a coord in the grid to the screen pixels
    def to_pixel (self, coord):
        return (coord[1] * self.grid_size, coord[0] * self.grid_size)

    # returns the block type at a certain location
    def get_block_type(self, row, col):
        self.check_valid(row, col)
        return self.grid[row][col]

    # checks if a location in a path block
    def is_path(self, row, col):
        self.check_valid(row, col)
        return self.get_block_type(row, col) == 'P'

    def is_corner(self, coord):
        return coord in self.corners and \
        self.corners.index(coord) != len(self.corners) - 1

    def turn_direction (self, corner):
        if self.is_corner(corner):
            index = self.corners.index(corner)
            if corner[0] == self.corners[index + 1][0]:
                if self.corners[index + 1][1] > corner[1]:
                    return 'R'
                else:
                    return 'L'
            elif corner[1] == self.corners[index + 1][1]:
                if self.corners[index + 1][0] > corner[0]:
                    return 'D'
                else:
                    return 'U'
            else:
                print("Unexpected error") 

    # checks if a rectangle object is on the path
    def on_path(self, rect):
        row_count = self.col_length()
        col_count = self.row_length()
        for row in range(0, row_count):
            for col in range(0, col_count):
                if self.is_path(row, col) and collide(col * self.grid_size, row * self.grid_size, self.grid_size, self.grid_size, rect.x, rect.y, rect.width, rect.height):
                    return True
        return False

    # checks if a rectangle in on a corner block
    def on_corner (self, rect, tolerance = 2):
        for corner in self.corners:
            if abs(self.to_pixel(corner)[0] - rect.topleft[0]) < tolerance and \
            abs(self.to_pixel(corner)[1] - rect.topleft[1]) < tolerance:
                return corner
        return False


    # starting_point
    # Find the starting pointing of the path if it exists, must start from left side of screen (for now)
    # Void -> (Int, Int)
    def starting_point(self):
        return self.to_pixel(self.corners[0])

    # Draws Map
    def draw (self, display, path_colour = WHITE):
        row_count = self.col_length()
        col_count = self.row_length()
        for row in range(0, row_count):
            for col in range(0, col_count):
                if self.is_path(row, col):
                    pygame.draw.rect(display, path_colour, [col * self.grid_size, row * self.grid_size, self.grid_size, self.grid_size])


class HP_Bar:
    def __init__(self, max_hp = 100, x = 0, y = 0, width = 200, height = 20, 
                colour_high = (0, 255, 0), colour_med = (255, 153, 51), colour_low = (255, 51, 51)):
        self.max_hp = max_hp
        self.hp = max_hp
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour_high = colour_high
        self.colour_med = colour_med
        self.colour_low = colour_low

    def increase_hp(self, value):
        self.hp = min(self.max_hp, self.hp + value)

    def decrease_hp(self, value):
        self.hp = max(0, self.hp - value)

    def set_hp(self, value):
        self.hp = value
        self.max_hp = max(self.max_hp, value)

    def increase_max_hp(self, value):
        self.max_hp = self.max_hp + value

    def decrease_max_hp(self, value):
        self.max_hp = max(0, self.max_hp - value)
        self.hp = min(self.max_hp, self.hp)

    def is_empty(self):
        return self.hp <= 0

    def percent_hp(self):
        if self.max_hp != 0:
            return round(float(self.hp) / self.max_hp, 2)
        return None

    def replenish(self):
        self.set_hp(self.max_hp)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), [self.x, self.y, self.width, self.height])
        if not self.is_empty():
            percent = self.percent_hp()
            colour = None
            if percent > 0.5:
                colour = self.colour_high
            elif percent > 0.3:
                colour = self.colour_med
            else:
                colour = self.colour_low
            pygame.draw.rect(screen, colour, [self.x, self.y, int(self.width * percent), self.height])

