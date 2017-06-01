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
        def __init__(self, body, colour, speed, screen_width, screen_height, hp):

            self.body = body 
            self.speed = speed 
            self.colour = colour 
            self.screen_width = screen_width
            self.screen_height = screen_height
            self.hp = hp


        def update(self):
            self.body.move_ip(self.speed)

        # Return true if the enemy has left the screen 
        def check_destroy(self):
            if self.body.left >= self.screen_width or self.hp <= 0:
                return True
            else:
                return False


class Bullet(object):

    def __init__(self, speed, pos, colour, screen_height, width = 5, height = 20):
        self.speed = speed
        # Inital position of the bullet ie. where the player made the shot 
        self.body = pygame.Rect(pos, (width, height))
        self.colour = colour 
        self.screen_height = screen_height 

    def update(self):
        self.body.move_ip(self.speed) 

    # Return true if the bullet leaves the screen 
    def check_destroy(self):
        if self.body.bottom >= self.screen_height:
            return True
        else:
            return False

class Tower(object):

    def __init__(self, pos):
        # moved space_between to properties
        self.pos = pos 
        self.level = 0
        self.type =  upgrade_list[self.level] # Each tower type will have a different colour  
        self.max_range = tower_range[self.type]  # Range is the radius 
        self.damage = tower_damage[self.type]
        self.cost = tower_cost[self.type] 
        self.body = pygame.Rect(self.pos, INITIAL_SIZE)


    def upgrade(self):
        self.level = self.level + 1 
        self.type =  upgrade_list[self.level] # Each tower type will have a different colour  
        self.max_range = tower_range[self.type]  # Range is the returnadius 
        self.damage = tower_damage[self.type]
        self.cost = tower_cost[self.type] 
        self.body.inflate_ip(tower_inflation[self.type])


