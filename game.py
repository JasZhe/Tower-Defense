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

# Mixer is for sounds
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# Map settings
game_map = Map('map2.txt')

# Grid dimensions
GRID_SIZE = game_map.grid_size

# Window size properties
WIDTH = game_map.cols * GRID_SIZE #1080
HEIGHT = game_map.rows * GRID_SIZE #720
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE) 
clock = pygame.time.Clock()

# Player info
player = Player(pygame.Rect((10, 10), (GRID_SIZE, GRID_SIZE)), BLUE, WIDTH, HEIGHT, 
    TICK_SPEED / FRAME_RATE, TICK_SPEED / FRAME_RATE, gun_colour = YELLOW)

# enemy stuff
enemy_list = [] 
enemy_start = game_map.starting_point()
counter = 0
spawn_time = 50
enemy_size = (GRID_SIZE, GRID_SIZE)
enemy_speed = RIGHT
enemy_initial_hp = 100 
enemy_max_hp = 100

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

# Sounds
rifle_gun = pygame.mixer.Sound(file="sounds/rifle_gun.wav")
sniper_gun = pygame.mixer.Sound(file="sounds/sniper_gun.wav")
machine_gun = pygame.mixer.Sound(file="sounds/machine_gun.wav")
player_gun = pygame.mixer.Sound(file="sounds/player_gun.wav")
heavy_gun = pygame.mixer.Sound(file="sounds/heavy_gun.wav")

explode_sound = pygame.mixer.Sound(file="sounds/explode_sound.wav")

tower_sounds = {
    "rifle" : rifle_gun,
    "sniper" : sniper_gun,
    "machine_gun" : machine_gun,
    "heavy" : heavy_gun
}

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

    if pressed[pygame.K_w]:
        for enemy in enemy_list:
            enemy.turn('U')
    if pressed[pygame.K_s]:
        for enemy in enemy_list:
            enemy.turn('D')
    if pressed[pygame.K_a]:
        for enemy in enemy_list:
            enemy.turn('L')
    if pressed[pygame.K_d]:
        for enemy in enemy_list:
            enemy.turn('R')

    if pressed[pygame.K_SPACE]:
        now = pygame.time.get_ticks()
        if now - last_shot >= SHOT_DELAY:
            pygame.mixer.Sound.play(player_gun)
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
        rand = random.randint(0,3)
        if rand == 0:
            tower_class = "rifle"
        elif rand == 1:
            tower_class = "sniper"
        elif rand == 2:
            tower_class = "machine_gun"
        elif rand == 3:
            tower_class = "heavy"

        temp = Tower((player.body.x, player.body.y),tower_class)
        placeable = True
        if game_map.on_path(player.body):
            placeable = False
        for tower in tower_list:
            if distance(temp.body.center, tower.body.center) <= space_between: 
                placeable = False
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
    

    # Draws path
    game_map.draw(screen, GRAY)

    
    # This loop is just used to draw the blocks used to signal turns for the enemies
    # comment out this loop when it's not needed anymore 
    #for turn in enemy_turn_list:
    #    pygame.draw.rect(screen, ORANGE, turn[0])

    for tower in tower_list:
        pygame.draw.rect(screen, tower.type, tower.body)
        
        # view range only when player is in range
        if distance(tower.body.center, player.body.center) <= 40:
            pygame.draw.circle(screen, GREEN, tower.body.center, tower.max_range, 1)

        # Tower range
        for enemy in enemy_list:
            if distance(tower.body.center, enemy.body.center) <= tower.max_range:
                # draws line to indicate hit for now
                #pygame.draw.lines(screen, RED, False, [tower.body.center, enemy.body.center], 2)

                if tower.canShoot():
                    pygame.mixer.Sound.play(tower_sounds[tower.tower_class])
                    dx = enemy.body.center[0] - tower.body.center[0]
                    dy = enemy.body.center[1] - tower.body.center[1]
                    quad = quadrant(tower.body, enemy.body)

                    # Vertical Case
                    if enemy.velocity[0] == 0:
                        # Quadratic formula to calculate impact time
                        time = quadratic_formula((enemy.velocity[1]**2 - tower.shell_speed**2), 2.0*enemy.velocity[1]*dy, dx**2 + dy**2)[1]
                        beta = math.acos(abs(dx / (tower.shell_speed * time)))
                    # Horizontal Case
                    else:
                        time = quadratic_formula((enemy.velocity[0]**2 - tower.shell_speed**2), 2.0*enemy.velocity[0]*dx, dx**2 + dy**2)[1]
                        beta = math.asin(abs(dy / (tower.shell_speed * time)))

                    # CAST rule accomodations
                    if quad == 1:
                        angle = beta
                    elif quad == 2:
                        angle = math.pi - beta
                    elif quad == 3:
                        angle = math.pi + beta 
                    else:
                        angle = 2.0 * math.pi - beta

                    if tower.tower_class == "machine_gun":
                        dispersion = random.randint(-15, 15) / 100.0
                        angle += dispersion

                    if tower.tower_class == "heavy":
                        w = 15
                        h = 15
                    else:
                        w = 5
                        h = 5


                    tower_bullets.append(
                        Bullet((tower.shell_speed * math.cos(angle), tower.shell_speed * math.sin(angle)),
                         tower.body.center, YELLOW, HEIGHT, w, h, damage = tower.damage))
                             
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
                enemy.hp = max(enemy.hp - SHOT_DMG, 0)
                bullet_list.remove(bullet)
        for bullet in tower_bullets:
            if bullet.body.colliderect(enemy.body):
                enemy.hp = max(enemy.hp - bullet.damage, 0)
                tower_bullets.remove(bullet)

                # AOE weapon
                if bullet.body.width == 15:
                    pygame.mixer.Sound.play(explode_sound)
                    for enemy in enemy_list:
                        if distance(bullet.body.center, enemy.body.center) <= 100:
                            enemy.hp = max(enemy.hp - bullet.damage * \
                            1 / (1 + math.sqrt(distance(bullet.body.center, enemy.body.center))/30),0)

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

        color = BLACK
        if enemy.hp > 0:
            if enemy.hp > 50:
                colour = GREEN
            elif enemy.hp > 30:
                colour = ORANGE
            else:
                colour = RED
      
        pygame.draw.rect(screen, colour, 
            [enemy.body.x, enemy.body.y + enemy.body.height - 5, enemy.body.width * enemy.hp / enemy.max_hp, 5])
        enemy.update()

    pygame.display.update()
    clock.tick(FRAME_RATE)
    counter = counter + 1 
