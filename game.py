import pygame, sys
from game_functions import *
from game_classes import *
from properties import *

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


pygame.init() 
screen = pygame.display.set_mode(SIZE) 
clock = pygame.time.Clock()

player = Player(pygame.Rect((10, 10), (30, 30)), BLUE, WIDTH, HEIGHT, 
    TICK_SPEED / FRAME_RATE, TICK_SPEED / FRAME_RATE)

# enemy stuff
enemy_list = [] 
counter = 0
spawn_rate = 50
enemy_size = (30, 30)
enemy_start = (10, HEIGHT / 2)

# Direction constants
RATE = 3 
RIGHT = (RATE, 0)
LEFT = (-RATE, 0)
UP = (0, -RATE)
DOWN = (0, RATE) 
enemy_speed = RIGHT

# Enemy pathing
turn_size = (45, 45)
enemy_turn_list = [(pygame.Rect((WIDTH / 4, HEIGHT / 2), turn_size), UP), 
                   (pygame.Rect((WIDTH / 4, HEIGHT / 8), turn_size), RIGHT),
                   (pygame.Rect((WIDTH - WIDTH / 4, HEIGHT / 8), turn_size), DOWN), 
                   (pygame.Rect((WIDTH - WIDTH / 4, HEIGHT - HEIGHT / 4), turn_size), RIGHT)]

# Bullet stuff 
bullet_list = [] 
last_shot = 0
SHOT_DELAY = 500
SHOT_DMG = 25
bullet_speed = (0, 10)

# Tower stuff 
tower_list = [] 
tower_damage = {GREEN : 5}
tower_cost = {GREEN : 10}
tower_size = {GREEN : (20, 20)}
tower_range = {GREEN : 160}

# Functions
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit() 

    # Every clock update the counter will increment by one, when spawn_rate
    # ticks have passed an enemy will spawn. 
    if counter % spawn_rate == 0:
        enemy_list.append(Enemy(pygame.Rect(enemy_start, enemy_size), RED,
                                enemy_speed, WIDTH, HEIGHT))

    for enemy in enemy_list:
        for turn in enemy_turn_list:
            if enemy.body.colliderect(turn[0]):
                enemy.speed = turn[1]

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
            bullet_list.append(Bullet(bullet_speed,((2 * player.body.x + player.body.width)/2 - 5/2, player.body.y), BLUE, HEIGHT))
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

    # This loop is just used to draw the blocks used to signal turns for the enemies
    # comment out this loop when it's not needed anymore 
    for turn in enemy_turn_list:
        pygame.draw.rect(screen, ORANGE, turn[0])

    for tower in tower_list:
        pygame.draw.rect(screen, tower.type, tower.body)
        # Tower range
        tower_pos = (round((2 * tower.body.x + tower.body.width)/2) , round((2 * tower.body.y + tower.body.height)/2))
        pygame.draw.circle(screen, GREEN, (round((2 * tower.body.x + tower.body.width)/2) ,round((2 * tower.body.y + tower.body.height)/2)), tower.max_range,1)
        for enemy in enemy_list:
            enemy_pos = ((2 * enemy.body.x + enemy.body.width)/2, (2 * enemy.body.y + enemy.body.height)/2)
            if distance(tower_pos, enemy_pos) <= tower.max_range:
                # draws line to indicate hit for now
                pygame.draw.lines(screen, RED, False, [tower_pos, enemy_pos], 2)

        # If the bullet leaves the screen then stop drawing the current bullet
        # and allow the player to make a new shot
    for bullet in bullet_list:
        if bullet.check_destroy():
            bullet_list.remove(bullet)

     # If the bullet is still on screen, draw it
    for bullet in bullet_list:
        pygame.draw.rect(screen, bullet.colour, bullet.body)
        bullet.update()

    # Draw each enemy and move it
    # If the enemy gets to the end of the screen remove it
    # Put draw and remove in different loops
    for enemy in enemy_list:
        for bullet in bullet_list:
            if bullet.body.colliderect(enemy.body):
                enemy.hp = enemy.hp - SHOT_DMG
                bullet_list.remove(bullet)

        if enemy.check_destroy():
            enemy_list.remove(enemy)

    for enemy in enemy_list:
        pygame.draw.rect(screen, enemy.colour, enemy.body)

        # HP Bar
        pygame.draw.rect(screen, BLACK, [enemy.body.x, enemy.body.y + enemy.body.height - 5, enemy.body.width, 5])
        #pygame.Rect((10, height / 2), (30, 30))

        color = BLACK
        if enemy.hp > 0:
            if enemy.hp > 50:
                colour = GREEN
            elif enemy.hp > 30:
                colour = ORANGE
            else:
                colour = RED
       # pygame.draw.rect(gameDisplay, colour, [ship_X, ship_Y + shipSize - 5, shipSize * hp / 100, 8])
        pygame.draw.rect(screen, colour, [enemy.body.x, enemy.body.y + enemy.body.height - 5, enemy.body.width * enemy.hp / 100, 5])
        enemy.update()

    pygame.display.flip()
    clock.tick(FRAME_RATE)
    counter = counter + 1 
