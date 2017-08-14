import pygame, sys
from functions import *
from properties import * 

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


class Sniper_Bullet(Bullet):
    def __init__(self, bullet):
        self.speed = bullet.speed
        self.body = bullet.body
        self.colour = bullet.colour 
        self.screen_height = bullet.screen_height
        self.screen_width = bullet.screen_width
        self.damage = bullet.damage 


class Heavy_Bullet(Bullet):
    def __init__(self, bullet):
        self.speed = bullet.speed
        self.body = bullet.body
        self.colour = bullet.colour 
        self.screen_height = bullet.screen_height
        self.screen_width = bullet.screen_width
        self.damage = bullet.damage 