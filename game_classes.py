import pygame, sys

# A module of all classes in the game
class Player(object): 

    def __init__(self, body, colour, screen_width, screen_height, x, y): 
        self.body = body
        self.colour = colour
        self.screen_width = screen_width
        self.screen_height = screen_height  
        self.horizontal_speed = x
        self.vertical_speed = y

    def update(self, x = 0, y = 0):

        # Make sure the player can't leave the screen. 

        if ((self.body.right >= self.screen_width and x > 0) or 
            (self.body.x <= 0 and x < 0)):

            self.body = self.body.move(0, y)
        elif ((self.body.bottom >= self.screen_height and y > 0) or 
            (self.body.y <= 0 and y < 0)):

            self.body = self.body.move(x, 0)
        else:
            self.body = self.body.move(x, y)


class Enemy(object):

        # Add health 
        def __init__(self, body, colour, speed, screen_width, screen_height, hp = 100):

            self.body = body 
            self.speed = speed 
            self.colour = colour 
            self.screen_width = screen_width
            self.screen_height = screen_height
            self.hp = hp


        def update(self):
            self.body = self.body.move(self.speed)

        # Return true if the enemy has left the screen 
        def check_destroy(self):
            if self.body.right >= self.screen_width or self.hp <= 0:
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
        self.body = self.body.move(self.speed) 

    # Return true if the bullet leaves the screen 
    def check_destroy(self):
        if self.body.bottom >= self.screen_height:
            return True
        else:
            return False

    # If the bullet hits an enemy, remove the enemy and return true
    # otherwise return false 
    # def check_hit(self, enemy_list):
    #   for enemy in enemy_list:
    #       if self.body.colliderect(enemy.body):
    #           enemy_list.remove(enemy)
    #           print "hit"
    #           return 1
    #       else:
    #           return 0

class Tower(object):

    def __init__(self, pos, colour, max_range, damage, cost, size):
        space_between = 40
        self.type = colour # Each tower type will have a different colour  
        self.max_range = max_range  # Range is the radius 
        self.damage = damage 
        self.cost = cost 
        self.body = pygame.Rect(pos, size)
        self.outer_body = pygame.Rect((pos[0] - self.body.width, pos[1] - self.body.height),
            (self.body.width + space_between, self.body.height + space_between))

