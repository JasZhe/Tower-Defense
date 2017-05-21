import pygame, sys

# Need to implement: 
#
# some way to create towers I'm thinking until I understand
# mouse movement I could have the player be a "builder" and he has to go 
# collect resources or something that could randomly appear on the map 
# in order to fill some sort of requirement to build a tower
#
# enemy health 
#
# a path that's not a straight line for the enemies to move in 
#
# a timer for build time 
#
# *************************************************************
# Extra ideas:
# 
# different towers
#
# replace rects with sprites 
#
# a nicer background 
#
# sound
#
# highscores or something
#
# different levels 
#
# *************************************************************
# Notes:
#
# should I allow the player to help kill enemies?
# for the tower range, create an invisible rect around the tower

#*************************************************************
# bullet_list = [] 
# bullet_delay = 0 
# if bullet_delay == 0 and pressed[pygame.K_SPACE]:
#   bullet_list.append() 
#   bullet_delay = 20 

# for bullet in bullet_list:
#   draw bullet 
#   update bullet 

# bullet_delay = bullet_delay - 1 
#
#***************************************************************


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
        def __init__(self, body, colour, speed, screen_width, screen_height):

            self.body = body 
            self.speed = speed 
            self.colour = colour 
            self.screen_width = screen_width
            self.screen_height = screen_height 


        def update(self):
            self.body = self.body.move(self.speed)

        # Return true if the enemy has left the screen 
        def check_destroy(self):
            if self.body.right >= self.screen_width: 
                return 1
            else:
                return 0 


class Bullet(object):

    def __init__(self, speed, pos, colour, screen_height):
        self.speed = speed
        # Inital position of the bullet ie. where the player made the shot 
        self.body = pygame.Rect(pos, (5, 20))
        self.colour = colour 
        self.screen_height = screen_height 

    def update(self):
        self.body = self.body.move(self.speed) 

    # Return true if the bullet leaves the screen 
    def check_destroy(self):
        if self.body.bottom >= self.screen_height:
            return 1
        else:
            return 0

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

BLUE = (0, 128, 255)
RED = (255, 51, 51)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
frame_rate = 30 
tick_speed = 300 
pygame.init() 

width = 1024
height = 768
size = (width, height) 
screen = pygame.display.set_mode(size) 

clock = pygame.time.Clock()

player = Player(pygame.Rect((10, 10), (30, 30)), BLUE, width, height, 
    tick_speed / frame_rate, tick_speed / frame_rate)

enemy_list = [] 
counter = 0
spawn_rate = 20
enemy_speed = (3, 0)

bullet_list = [] 
last_shot = 0
SHOT_DELAY = 500

tower_list = [] 
tower_damage = {GREEN : 5}
tower_cost = {GREEN : 10}
tower_size = {GREEN : (20, 20)}
tower_range = {GREEN : 20}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit() 

    # Every clock update the counter will increment by one, when spawn_rate
    # ticks have passed an enemy will spawn. 
    if counter % spawn_rate == 0:

        enemy_list.append(Enemy(pygame.Rect((10, height / 2), (30, 30)), RED, 
            enemy_speed, width, height))


    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        player.update(y = -player.vertical_speed)
    if pressed[pygame.K_DOWN]:
        player.update(y = player.vertical_speed)
    if pressed[pygame.K_LEFT]:
        player.update(x = -player.horizontal_speed)
    if pressed[pygame.K_RIGHT]:
        player.update(x = player.horizontal_speed)

    if pressed[pygame.K_SPACE]:
        now = pygame.time.get_ticks()
        if now - last_shot >= SHOT_DELAY:
            bullet_list.append(Bullet((0, 10),(player.body.x, player.body.y), BLUE, height))
            last_shot = now

    if pressed[pygame.K_t]:
        temp = Tower((player.body.x, player.body.y), GREEN, tower_range[GREEN], 
            tower_damage[GREEN], tower_cost[GREEN], tower_size[GREEN])
        placeable = 1 
        for tower in tower_list:
            if temp.body.colliderect(tower.outer_body):
                placeable = 0
                break
        if placeable:
            tower_list.append(temp)


    screen.fill(BLACK) 
    pygame.draw.rect(screen, player.colour, player.body)

    for tower in tower_list:
        pygame.draw.rect(screen, tower.type, tower.body)

    # If the player made a shot draw the bullet
    for bullet in bullet_list:
        pygame.draw.rect(screen, bullet.colour, bullet.body)
        bullet.update()
        # If the bullet leaves the screen then stop drawing the current bullet
        # and allow the player to make a new shot
    for bullet in bullet_list:
        if bullet.check_destroy():
            bullet_list.remove(bullet)

    # Draw each enemy and move it
    # If the enemy gets to the end of the screen remove it
    # Put draw and remove in different loops
    for enemy in enemy_list:
        if enemy.check_destroy():
            enemy_list.remove(enemy)
        for bullet in bullet_list:
            if bullet.body.colliderect(enemy.body):
                enemy_list.remove(enemy)
                bullet_list.remove(bullet)

    for enemy in enemy_list:
        pygame.draw.rect(screen, enemy.colour, enemy.body)
        enemy.update()

    pygame.display.flip()
    clock.tick(frame_rate)
    counter = counter + 1 
