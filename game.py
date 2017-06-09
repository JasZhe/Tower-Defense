import pygame, sys
from functions import *
from classes import *
from properties import *

# Need to implement: 
#
# some way to create towers I'm thinking until I understand
# mouse movement I could have the player be a "builder" and he has to go 
# collect resources or something that could randomly appear on the map 
# in order to fill some sort of requirement to build a tower
#
# *DONE* enemy health
#
# *DONE* a path that's not a straight line for the enemies to move in
#
# a timer for build time 
#
# player resources 
#
# tower build time -nah?
#
# towet build cost
#
# some way for the game to end, ie if a certain number of enemies pass through 
#       Base HP: each enemy that breaks through reduces it
#
# variety of enemies
#
# enemies being able to kill the player and player has a death timer 
#
# *************************************************************
# Extra ideas:
# 
# *DONE* different towers
#
# Different types of towers (Fast shooting, slow shooting, splash damage, slow enemy)
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
#       Circle is better * DONE

#*************************************************************


pygame.init() 
screen = pygame.display.set_mode(SIZE) 
clock = pygame.time.Clock()

player = Player(pygame.Rect((10, 10), (30, 30)), BLUE, WIDTH, HEIGHT, 
    TICK_SPEED / FRAME_RATE, TICK_SPEED / FRAME_RATE, gun_colour = YELLOW)

# enemy stuff
enemy_list = [] 

# Enemy pathing
turn_size = (45, 45)
enemy_turn_list = [(pygame.Rect((WIDTH / 4, HEIGHT / 2), turn_size), UP), 
                   (pygame.Rect((WIDTH / 4, HEIGHT / 8), turn_size), RIGHT),
                   (pygame.Rect((WIDTH - WIDTH / 4, HEIGHT / 8), turn_size), DOWN), 
                   (pygame.Rect((WIDTH - WIDTH / 4, HEIGHT - HEIGHT / 4), turn_size), RIGHT)]

# Bullet stuff 
bullet_list = [] 
tower_bullets = []
last_shot = 0
bullet_speed_x = 0
bullet_speed_y = 20
bullet_speed = (bullet_speed_x, bullet_speed_y)

# Tower stuff 
# moved the tower stuff to properties 
tower_list = [] 
last_upgrade = 0 

# testing stuff 
spawn_increase_time = 0 
spawn_decrease_time = 0
increase_enemy_health_time = 0 
myfont = pygame.font.SysFont("monospace", 15)
label = myfont.render("Health: %d SpawnRate: %d" % (enemy_initial_hp, spawn_time), 
    1, (255, 255, 255))
screen.blit(label, (100, 100))

# Main Gameloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit() 

    # Every clock update the counter will increment by one, when spawn_time
    # ticks have passed an enemy will spawn. 
    if counter % spawn_time == 0:
        enemy_list.append(Enemy(pygame.Rect(enemy_start, enemy_size), RED,
                                enemy_speed, WIDTH, HEIGHT, enemy_initial_hp, enemy_max_hp))

    for enemy in enemy_list:
        for turn in enemy_turn_list:
            if enemy.body.colliderect(turn[0]):
                enemy.speed = turn[1]

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        player.update(y = -player.vertical_speed)
        player.direction = "U"
        bullet_speed = (bullet_speed_x, -bullet_speed_y)
    if pressed[pygame.K_DOWN]:
        player.update(y = player.vertical_speed)
        player.direction = "D"
        bullet_speed = (bullet_speed_x, bullet_speed_y)
    if pressed[pygame.K_LEFT]:
        player.update(x = -player.horizontal_speed)
        player.direction = "L"
        bullet_speed = (-bullet_speed_y, bullet_speed_x)
    if pressed[pygame.K_RIGHT]:
        player.update(x = player.horizontal_speed)
        player.direction = "R"
        bullet_speed = (bullet_speed_y, bullet_speed_x)

    if pressed[pygame.K_SPACE]:
        now = pygame.time.get_ticks()
        if now - last_shot >= SHOT_DELAY:
            if player.direction == "U" or player.direction == "D":
                w = SHOT_WIDTH
                h = SHOT_HEIGHT
            else:
                w = SHOT_HEIGHT
                h = SHOT_WIDTH
            bullet_list.append(Bullet(bullet_speed, 
                coord_add(player.body.center, (
                    -w/2, -h/2)), YELLOW, HEIGHT, w, h))
            last_shot = now
            #bullet_speed = (bullet_speed[0] + 0.1, bullet_speed[1])
           # print(bullet_speed)

    if pressed[pygame.K_t]:
        temp = Tower((player.body.x, player.body.y))
        placeable = 1 
        for tower in tower_list:
            if distance(temp.body.center, tower.body.center) <= space_between: 
                placeable = 0
                break
        if placeable:
            tower_list.append(temp)

    if pressed[pygame.K_g]:
        for tower in tower_list:
            if player.body.colliderect(tower.body):
                tower_list.remove(tower)
                break

    if pressed[pygame.K_u]:
        now = pygame.time.get_ticks()
        if now - last_upgrade >= UPGRADE_DELAY: 
            for tower in tower_list:
                if player.body.colliderect(tower.body):
                    if tower.level < tower_max_level:
                        tower.upgrade()
                        last_upgrade = now 
                    break

# ***************** TESTING COMMANDS ********************************

    # increases spawn rate for testing purposes
    if pressed[pygame.K_p]:
        now = pygame.time.get_ticks()
        if now - spawn_increase_time >= 100 and spawn_time > 15:
            spawn_time = spawn_time - 5
            spawn_increase_time = now

    # decreases spawn rate
    if pressed[pygame.K_o]:
        now = pygame.time.get_ticks()
        if now - spawn_decrease_time >= 100 and spawn_time < 200:
            spawn_time = spawn_time + 5
            spawn_decrease_time = now

    # increase enemy health 
    if pressed[pygame.K_h]:
        now = pygame.time.get_ticks()
        if now - increase_enemy_health_time >= 100 and enemy_initial_hp <= 500:
            enemy_initial_hp = enemy_initial_hp + 5
            enemy_max_hp = enemy_max_hp + 5
            for enemy in enemy_list:
                enemy.hp = enemy_initial_hp 
            increase_enemy_health_time = now

    # decrease enemy health 
    if pressed[pygame.K_j]:
        now = pygame.time.get_ticks()
        if now - increase_enemy_health_time >= 100 and enemy_initial_hp >= 10:
            enemy_initial_hp = enemy_initial_hp - 5 
            for enemy in enemy_list:
                enemy.hp = enemy_initial_hp 
            increase_enemy_health_time = now

    label = myfont.render("Health: %d Spawn Time: %d" % (enemy_initial_hp, spawn_time), 
        1, (255, 255, 255))

# ***************** TESTING COMMANDS ********************************


    screen.fill(BLACK) 
    screen.blit(label, (10, 10))
    
    # This loop is just used to draw the blocks used to signal turns for the enemies
    # comment out this loop when it's not needed anymore 
    for turn in enemy_turn_list:
        pygame.draw.rect(screen, ORANGE, turn[0])

    for tower in tower_list:
        pygame.draw.rect(screen, tower.type, tower.body)
        
        # view range only when player is in range
        if distance(tower.body.center, player.body.center) <= tower.max_range:
            pygame.draw.circle(screen, GREEN, tower.body.center, tower.max_range, 1)

        # Tower range
        for enemy in enemy_list:
            if distance(tower.body.center, enemy.body.center) <= tower.max_range:
                # draws line to indicate hit for now
                pygame.draw.lines(screen, RED, False, [tower.body.center, enemy.body.center], 2)

                if tower.canShoot():
                    #if enemy.body.x - tower.body.x == 0:
                    c = (enemy.body.center[1] - tower.body.center[1]) * 1.0 / (enemy.body.center[0] - tower.body.center[0])
                    if enemy.speed[0] == 0: 
                        angle = math.acos(-enemy.speed[1] * 1.0 / (tower.shellSpeed * math.sqrt(1.0 + c * c))) - math.atan(1/c)

                        
                        # CAST rule accomodation
                        if (c > 0 and enemy.body.center[1] - tower.body.center[1] <= 0) or \
                            (c < 0 and enemy.body.center[1] - tower.body.center[1] <= 0):


                            angle += math.pi
                        tower_bullets.append(
                            Bullet((tower.shellSpeed*math.cos(angle), tower.shellSpeed*math.sin(angle)),
                             tower.body.center, YELLOW, HEIGHT, width = 5, height = 5))

                # now based on the tower damage specified in the properties file 
                #enemy.hp = enemy.hp - tower.damage
                break
        tower.time += 1

    for bullet in tower_bullets:
        if bullet.check_destroy():
            tower_bullets.remove(bullet)

    for bullet in tower_bullets:
        pygame.draw.rect(screen, bullet.colour, bullet.body)
        bullet.update()
    # If the bullet leaves the screen then stop drawing the current bullet
    # and allow the player to make a new shot
    for bullet in bullet_list:
        if bullet.check_destroy():
            bullet_list.remove(bullet)

     # If the bullet is still on screen, draw it
    for bullet in bullet_list:
        pygame.draw.rect(screen, bullet.colour, bullet.body)
        bullet.update()
    player.draw(screen)
    

    # Draw each enemy and move it
    # If the enemy gets to the end of the screen remove it
    # Put draw and remove in different loops
    for enemy in enemy_list:
        for bullet in bullet_list:
            if bullet.body.colliderect(enemy.body):
                enemy.hp = enemy.hp - SHOT_DMG
                bullet_list.remove(bullet)
        for bullet in tower_bullets:
            if bullet.body.colliderect(enemy.body):
                enemy.hp = enemy.hp - tower.damage
                tower_bullets.remove(bullet)

        if enemy.check_destroy():
            enemy_list.remove(enemy)


    # Draw enemy if still alive at the end of the frame
    for enemy in enemy_list:
        pygame.draw.rect(screen, enemy.colour, enemy.body)

        # Enemy info
        screen.blit(myfont.render("HP: %d/%d" % (enemy.hp, enemy.max_hp), 
            1, (255, 255, 255)), enemy.body.bottomleft)

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
        pygame.draw.rect(screen, colour, 
            [enemy.body.x, enemy.body.y + enemy.body.height - 5, enemy.body.width * enemy.hp / enemy.max_hp, 5])
        enemy.update()

    pygame.display.update()
    clock.tick(FRAME_RATE)
    counter = counter + 1 
