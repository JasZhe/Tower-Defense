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

class Player(object): 

	def __init__(self, body, colour, screen_width, screen_height): 
		self.body = body
		self.colour = colour
		self.screen_width = screen_width
		self.screen_height = screen_height  

	def update(self, x, y):

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
	# 	for enemy in enemy_list:
	# 		if self.body.colliderect(enemy.body):
	# 			enemy_list.remove(enemy)
	# 			print "hit"
	# 			return 1
	# 		else:
	# 			return 0

class Tower(object):

	def __init__(self, pos, colour, max_range, damage, cost):
		self.colour = colour 
		self.max_range = max_range 
		self.damage = damage 
		self.cost = cost 


BLUE = (0, 128, 255)
RED = (255, 51, 51)
pygame.init() 

width = 1024
height = 768
size = (width, height) 
black = (0, 0, 0)
screen = pygame.display.set_mode(size) 

clock = pygame.time.Clock()

player = Player(pygame.Rect((10, 10), (30, 30)), BLUE, width, height)

enemy_list = [] 
counter = 0
spawn_rate = 20
enemy_speed = (3, 0)

bullet_list = [] 
shot_made = 0

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit() 

	# Every clock update the counter will increment by one, when spawn_rate
	# ticks have passed an enemy will spawn. 
	if counter % spawn_rate	== 0:

		enemy_list.append(Enemy(pygame.Rect((10, height / 2), (30, 30)), RED, 
			enemy_speed, width, height))


	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_UP]:
		player.update(0, -5)
	if pressed[pygame.K_DOWN]:
		player.update(0, 5)
	if pressed[pygame.K_LEFT]:
		player.update(-5, 0)
	if pressed[pygame.K_RIGHT]:
		player.update(5, 0)

	if pressed[pygame.K_SPACE] and not shot_made:
		bullet = Bullet((0, 10), 
			(player.body.x, player.body.y), BLUE, height)
		shot_made = 1 

	screen.fill(black) 
	pygame.draw.rect(screen, player.colour, player.body)

	# If the player made a shot draw the bullet
	if shot_made:
		pygame.draw.rect(screen, bullet.colour, bullet.body)
		bullet.update()
		# If the bullet leaves the screen then stop drawing the current bullet
		# and allow the player to make a new shot 
		if bullet.check_destroy():
			shot_made = 0

	# Draw each enemy and move it
	# If the enemy gets to the end of the screen remove it
	for enemy in enemy_list:
		pygame.draw.rect(screen, enemy.colour, enemy.body)
		enemy.update()
		if enemy.check_destroy():
			enemy_list.remove(enemy)
		if shot_made:
			if bullet.body.colliderect(enemy.body):
				enemy_list.remove(enemy)
				shot_made = 0

	pygame.display.flip()
	clock.tick(60)
	counter = counter + 1 
