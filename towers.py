import pygame, sys
from functions import *
from properties import * 
from classes import *
from bullets import * 

class Tower(object):
    def __init__(self, pos): #, tower_class = "rifle"):
        # moved space_between to properties
        # shellSpeed should be >= 10, anything smaller will create rounding inaccuracies
        self.pos = pos 
        self.level = 0   
        self.type =  upgrade_list[self.level] # Each tower type will have a different colour  
        self.body = pygame.Rect(self.pos, INITIAL_SIZE)
        self.time = 0
        self.angle = 0 #bullet angle 

    def upgrade(self):
        self.level = self.level + 1         
        self.type =  upgrade_list[self.level] # Each tower type will have a different colour  

    # shoots at enemy when time is right
    def canShoot(self):
        print "undefined"

    # Calculates damage rate (Damage Per Frame)
    def dpm(self):
        print "undefined"

    def shoot(self, enemy, HEIGHT, WIDTH): 
        if self.canShoot():
            pygame.mixer.Sound.play(self.sound)
            dx = enemy.body.center[0] - self.body.center[0]
            dy = enemy.body.center[1] - self.body.center[1]
            quad = quadrant(self.body, enemy.body)

            # Vertical Case
            if enemy.velocity[0] == 0:
                # Quadratic formula to calculate impact time
                time = quadratic_formula((enemy.velocity[1]**2 - self.shell_speed**2), 2.0*enemy.velocity[1]*dy, dx**2 + dy**2)[1]
                beta = math.acos(abs(dx / (self.shell_speed * time)))
            # Horizontal Case
            else:
                time = quadratic_formula((enemy.velocity[0]**2 - self.shell_speed**2), 2.0*enemy.velocity[0]*dx, dx**2 + dy**2)[1]
                beta = math.asin(abs(dy / (self.shell_speed * time)))

            # CAST rule accomodations
            if quad == 1:
                self.angle = beta
            elif quad == 2:
                self.angle = math.pi - beta
            elif quad == 3:
                self.angle = math.pi + beta 
            else:
                self.angle = 2.0 * math.pi - beta

            w = 5
            h = 5

            bullet = Bullet((self.shell_speed * math.cos(self.angle), self.shell_speed * math.sin(self.angle)),
                 self.body.center, YELLOW, HEIGHT, WIDTH, w, h, damage = self.damage)

            return bullet 


class Rifle_Tower(Tower): 

    damage_levels = {GREEN : 5, CYAN : 6, BLUE : 7, DARK_BLUE : 8, YELLOW : 9, ORANGE : 10,
                MAGENTA : 12, WHITE : 14}

    cost_levels = {GREEN : 50, CYAN : 100, BLUE : 150, DARK_BLUE : 200, YELLOW : 300, ORANGE : 400,
                MAGENTA : 600, WHITE : 800}

    inflation = {GREEN : (0, 0), CYAN : (0, 0), BLUE : (10, 10), DARK_BLUE : (0, 0), 
                YELLOW : (5, 5), ORANGE : (0, 0), MAGENTA : (5, 5), WHITE : (5, 5)}

    att_range = {GREEN : 240, CYAN : 260, BLUE : 280, DARK_BLUE : 300, YELLOW : 310, ORANGE : 320,
                MAGENTA : 330, WHITE : 340}

    reload_speed = 4

    shell_speed = 15

    def __init__(self, pos): 
        super(Rifle_Tower, self).__init__(pos)
        self.max_range = self.att_range[self.type]
        self.damage = self.damage_levels[self.type]
        self.cost = self.cost_levels[self.type]
        self.reload_speed = self.reload_speed 
        self.shell_speed = self.shell_speed
        self.sound = pygame.mixer.Sound(file="sounds/rifle_gun.wav")

    def upgrade(self): 
        super(Rifle_Tower, self).upgrade() 
        self.max_range = self.att_range[self.type] 
        self.damage = self.damage_levels[self.type]
        self.cost = self.cost_levels[self.type] 
        self.body.inflate_ip(self.inflation[self.type])

    def canShoot(self):
        if self.time % self.reload_speed == 0:
            self.time = 0
            return True
        else:
            return False

    def dpm(self):
        return self.damage / self.reload_speed

    def shoot(self, enemy, HEIGHT, WIDTH):
        bullet = super(Rifle_Tower, self).shoot(enemy, HEIGHT, WIDTH)
        return bullet


class Sniper_Tower(Tower): 

    damage_levels = {GREEN : 80, CYAN : 90, BLUE : 100, DARK_BLUE : 120, YELLOW : 140, ORANGE : 160,
                MAGENTA : 180, WHITE : 200}

    cost_levels = {GREEN : 50, CYAN : 100, BLUE : 150, DARK_BLUE : 200, YELLOW : 300, ORANGE : 400,
                MAGENTA : 600, WHITE : 800}

    inflation = {GREEN : (0, 0), CYAN : (0, 0), BLUE : (10, 10), DARK_BLUE : (0, 0), 
                YELLOW : (5, 5), ORANGE : (0, 0), MAGENTA : (5, 5), WHITE : (5, 5)}

    att_range = {GREEN : 240, CYAN : 260, BLUE : 280, DARK_BLUE : 300, YELLOW : 310, ORANGE : 320,
                MAGENTA : 330, WHITE : 340}

    reload_speed = 90

    shell_speed = 30

    def __init__(self, pos): 
        super(Sniper_Tower, self).__init__(pos)
        self.max_range = self.att_range[self.type]
        self.damage = self.damage_levels[self.type]
        self.cost = self.cost_levels[self.type]
        self.reload_speed = self.reload_speed 
        self.shell_speed = self.shell_speed
        self.sound = pygame.mixer.Sound(file="sounds/sniper_gun.wav")

    def upgrade(self): 
        super(Sniper_Tower, self).upgrade() 
        self.max_range = self.att_range[self.type] 
        self.damage = self.damage_levels[self.type]
        self.cost = self.cost_levels[self.type] 
        self.body.inflate_ip(self.inflation[self.type])

    def canShoot(self):
        if self.time % self.reload_speed == 0:
            self.time = 0
            return True
        else:
            return False

    def dpm(self):
        return self.damage / self.reload_speed

    
    def shoot(self, enemy, HEIGHT, WIDTH):
        bullet = super(Sniper_Tower, self).shoot(enemy, HEIGHT, WIDTH)
        if bullet is not None:
            bullet = Sniper_Bullet(bullet)
        return bullet 
    

class MachineGun_Tower(Tower): 
    damage_levels = {GREEN : 5, CYAN : 6, BLUE : 7, DARK_BLUE : 8, YELLOW : 9, ORANGE : 10, MAGENTA : 12, WHITE : 14}

    cost_levels = {GREEN : 50, CYAN : 100, BLUE : 150, DARK_BLUE : 200, YELLOW : 300, ORANGE : 400, MAGENTA : 600, WHITE : 800}

    inflation = {GREEN : (0, 0), CYAN : (0, 0), BLUE : (10, 10), DARK_BLUE : (0, 0), YELLOW : (5, 5), ORANGE : (0, 0), MAGENTA : (5, 5), WHITE : (5, 5)}

    att_range = {GREEN : 240, CYAN : 260, BLUE : 280, DARK_BLUE : 300, YELLOW : 310, ORANGE : 320, MAGENTA : 330, WHITE : 340}

    reload_speed = 4

    shell_speed = 15

    def __init__(self, pos): 
        super(MachineGun_Tower, self).__init__(pos)
        self.max_range = self.att_range[self.type]
        self.damage = self.damage_levels[self.type]
        self.cost = self.cost_levels[self.type]
        self.reload_speed = self.reload_speed 
        self.shell_speed = self.shell_speed
        self.sound = pygame.mixer.Sound(file="sounds/machine_gun.wav")

    def upgrade(self): 
        super(MachineGun_Tower, self).upgrade() 
        self.max_range = self.att_range[self.type] 
        self.damage = self.damage_levels[self.type]
        self.cost = self.cost_levels[self.type] 
        self.body.inflate_ip(self.inflation[self.type])

    def canShoot(self):
        if self.time % self.reload_speed == 0:
            self.time = 0
            return True
        else:
            return False

    def dpm(self):
        return self.damage / self.reload_speed

    def shoot(self, enemy, HEIGHT, WIDTH):
        bullet = super(MachineGun_Tower, self).shoot(enemy, HEIGHT, WIDTH)

        if bullet is not None: 
            dispersion = random.randint(-15, 15) / 100.0
            self.angle += dispersion
            bullet.speed = (self.shell_speed * math.cos(self.angle), self.shell_speed * math.sin(self.angle))
            return bullet 


class HeavyGun_Tower(Tower): 

    damage_levels = {GREEN : 5, CYAN : 6, BLUE : 7, DARK_BLUE : 8, YELLOW : 9, ORANGE : 10,
                MAGENTA : 12, WHITE : 14}

    cost_levels = {GREEN : 50, CYAN : 100, BLUE : 150, DARK_BLUE : 200, YELLOW : 300, ORANGE : 400,
                MAGENTA : 600, WHITE : 800}

    inflation = {GREEN : (0, 0), CYAN : (0, 0), BLUE : (10, 10), DARK_BLUE : (0, 0), 
                YELLOW : (5, 5), ORANGE : (0, 0), MAGENTA : (5, 5), WHITE : (5, 5)}

    att_range = {GREEN : 240, CYAN : 260, BLUE : 280, DARK_BLUE : 300, YELLOW : 310, ORANGE : 320,
                MAGENTA : 330, WHITE : 340}

    reload_speed = 4

    shell_speed = 15

    def __init__(self, pos): 
        super(HeavyGun_Tower, self).__init__(pos)
        self.max_range = self.att_range[self.type]
        self.damage = self.damage_levels[self.type]
        self.cost = self.cost_levels[self.type]
        self.reload_speed = self.reload_speed 
        self.shell_speed = self.shell_speed
        self.sound = pygame.mixer.Sound(file="sounds/heavy_gun.wav")

    def upgrade(self): 
        super(HeavyGun_Tower, self).upgrade() 
        self.max_range = self.att_range[self.type] 
        self.damage = self.damage_levels[self.type]
        self.cost = self.cost_levels[self.type] 
        self.body.inflate_ip(self.inflation[self.type])

    def canShoot(self):
        if self.time % self.reload_speed == 0:
            self.time = 0
            return True
        else:
            return False

    def dpm(self):
        return self.damage / self.reload_speed


    def shoot(self, enemy, HEIGHT, WIDTH): 
        bullet = super(HeavyGun_Tower, self).shoot(enemy, HEIGHT, WIDTH)

        if bullet is not None: 
            bullet = Heavy_Bullet(bullet)
            bullet.body.width = 15
            bullet.body.height = 15
            return bullet 