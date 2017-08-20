import pygame, sys
from functions import *
from properties import * 
from bullets import *
from classes import HP_Bar

class Enemy(object):
        # Add health 
        def __init__(self, body, colour, velocity, screen_width, screen_height, hp, max_hp = 100):

            self.body = body 
            self.velocity = velocity # Tuple (v_x, v_y)
            self.colour = colour 
            self.screen_width = screen_width
            self.screen_height = screen_height
            self.hp_bar = HP_Bar(max_hp, body.x, body.y - 5, body.width, 5)


        def update(self):
            self.body.move_ip(self.velocity)

        # Return true if the enemy has left the screen or destroyed
        def check_destroy(self, percent_margin = 0.2):
            if self.hp_bar.is_empty() \
            or self.body.top > self.screen_height * (1 + percent_margin) \
            or self.body.bottom < 0 - self.screen_height * percent_margin \
            or self.body.left > self.screen_width * (1 + percent_margin) \
            or self.body.right < 0 - self.screen_width * percent_margin:
                return True
            else:
                return False

        def breach(self, percent_margin  = 0.2):
            return not self.hp_bar.is_empty() and self.check_destroy(percent_margin)

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
            explosion_radius = 60

            if type(bullet) is Heavy_Bullet:
                if distance(bullet.body.center, self.body.center) <= explosion_radius:
                    self.hp_bar.decrease_hp(bullet.damage * \
                                1 / (1 + distance(bullet.body.center, self.body.center) /explosion_radius))

            else:
                self.hp_bar.decrease_hp(bullet.damage)

        def draw(self, screen):
            pygame.draw.rect(screen, self.colour, self.body)
            print("BODY")
            self.hp_bar.draw(screen, self.body.x, self.body.bottom - self.hp_bar.height)

        def __str__(self):
            return "===" + str(self.hp_bar.hp) + "==="


class Shield_Enemy(Enemy):

    def __init__(self, body, colour, velocity, screen_width, screen_height, hp, max_hp = 100, shield_hp = 100):
        super().__init__(body, colour, velocity, screen_width, screen_height, hp, max_hp = 100)
        self.shield_hp = shield_hp
        self.max_shield = shield_hp
        self.shield_bar = HP_Bar(shield_hp, body.x, body.y - 10, body.width, 5, WHITE, WHITE, WHITE, None)

    # Shield guys not affected by aoe damage 
    # Shield takes double damage
    # Bring the shield below 0 does not affect regular hp 
    def damage(self, bullet):
        if self.shield_bar.is_empty(): 
            super().damage(bullet)
        else: 
            if type(bullet) is Heavy_Bullet:
                if distance(bullet.body.center, self.body.center) <= 100:
                    self.shield_hp = max(self.shield_hp - bullet.damage * \
                                1 / (1 + distance(bullet.body.center, self.body.center)/60), 0)
                    self.shield_bar.decrease_hp(bullet.damage * \
                                1 / (1 + distance(bullet.body.center, self.body.center)/60))
            else:
                self.shield_bar.decrease_hp(2 * bullet.damage)
    
    def draw(self, screen):
        print("SHIELD")
        super().draw(screen)
        self.shield_bar.draw(screen, self.body.x, self.body.bottom - self.hp_bar.height - self.shield_bar.height)

