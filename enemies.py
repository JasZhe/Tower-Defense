import pygame, sys
from functions import *
from properties import * 
from bullets import *

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

        def breach(self, percent_margin  = 0.2):
            return self.hp > 0 and self.check_destroy(percent_margin)

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

        def check_hit(self, bullet):
            return bullet.body.colliderect(self.body)

        # if bullet collides with enemy, subtract the damage of the bullet from hp 
        def damage(self, bullet):
            explosion_radius = 200

            if type(bullet) is Heavy_Bullet:
                if distance(bullet.body.center, self.body.center) <= explosion_radius:
                    self.hp = max(self.hp - bullet.damage * \
                                1 / (1 + math.sqrt(distance(bullet.body.center, self.body.center))/30),0)

            else:
                self.hp = max(self.hp - bullet.damage, 0)


class Shield_Enemy(Enemy):

    def __init__(self, enemy, shield_hp = 100):
            self.body = enemy.body 
            self.velocity = enemy.velocity # Tuple (v_x, v_y)
            self.colour = enemy.colour
            self.screen_width = enemy.screen_width
            self.screen_height = enemy.screen_height
            self.hp = enemy.hp
            self.max_hp = enemy.max_hp
            self.shield_hp = shield_hp
            self.max_shield = shield_hp 

    # Shield guys not affected by aoe damage 
    # Shield takes double damage
    # Bring the shield below 0 does not affect regular hp 
    def damage(self, bullet):
        if self.shield_hp == 0: 
            super(Shield_Enemy, self).damage(bullet)
        else: 
            if type(bullet) is Heavy_Bullet:
                if distance(bullet.body.center, self.body.center) <= 100:
                        self.shield_hp = max(self.shield_hp - bullet.damage * \
                                    1 / (1 + math.sqrt(distance(bullet.body.center, self.body.center))/30), 0)
            else:
                self.shield_hp = max(self.shield_hp - (2 * bullet.damage), 0)
        
