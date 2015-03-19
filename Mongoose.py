"""
Created on:  March 4, 2014
Created by:  Alex Neuenkirk && Ren C'DeBaca
"""
import sys
import pygame
import math
import Snake_Class
import random
import pathfindAstar as pathfinder
from baby_mongoose import Baby
from mongoose_player import Player


colors = {'white': (255, 255, 255),
		  'black': (0, 0, 0),
		  'red': (255, 0, 0),
		  'yellow': (255, 255, 0),
		  'orange': (255, 127, 39),
		  'green': (0, 255, 0),
		  'blue': (0, 0, 255),
		  'pink': (255, 128, 192),
		  'purple': (128, 0, 255),
		  'light_blue': (0, 128, 255),
		  'cyan': (0, 255, 255),
		  'blood': (175, 0, 0),
		  'gray': (25, 25, 25),
		  'bufferZone': (70, 35, 0),
		  'bufferFill': (21, 11, 0)}

# DISPLAY VARIABLES
tile_size = 35
margin = 0
zoneHeight = 50
deltaTime = 0

# INITIALIZE BABY STARTING POSITIONS
babyStart1 = Baby.spawnLocations.pop(random.randint(0, len(Baby.spawnLocations) - 1))
babyStart2 = Baby.spawnLocations.pop(random.randint(0, len(Baby.spawnLocations) - 1))
babyStart3 = Baby.spawnLocations.pop(random.randint(0, len(Baby.spawnLocations) - 1))
babyStart4 = Baby.spawnLocations.pop(random.randint(0, len(Baby.spawnLocations) - 1))
babyStart5 = Baby.spawnLocations.pop(random.randint(0, len(Baby.spawnLocations) - 1))

# SAVE THE BABY POSITIONS INTO A LIST
babyStarts = [babyStart1, babyStart2, babyStart3, babyStart4, babyStart5]

# CREATE BABY OBJECTS
baby1 = Baby(babyStart1)
baby2 = Baby(babyStart2)
baby3 = Baby(babyStart3)
baby4 = Baby(babyStart4)
baby5 = Baby(babyStart5)

# ADD BABY OBJECTS INTO A LIST
babies = [baby1, baby2, baby3, baby4, baby5]

# ADD THESE POSITIONS TO BABY'S CLASS VARIABLE
for i in range(len(babyStarts)):
	Baby.currentLocations.append(babyStarts[i])

# CREATE THE BOARD
board = pathfinder.Board(35, 19)
board.generateObstacles()

# GET OBSTACLE LOCATION INFORMATION FROM THE BOARD
rocks = board.rocks
cacti = board.cacti
obstacles = board.obstacles  # For all obstacles

# CREATE THE PLAYER OBJECT
player = Player([0, 0])
player.pixX = player.x * tile_size
player.pixY = player.y * tile_size
horizontal_speed = 65
vertical_speed = 40

# PYGAME VARIABLES
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((board.width * tile_size, board.height * tile_size))
pygame.display.set_caption("MONGOOSE")
screen.fill(colors['bufferFill'])

# SPRITES
desert_sprite = pygame.image.load("desert1.png").convert_alpha()
cacti_sprites = pygame.image.load("cacti.png").convert_alpha()
Baby.load_sprites()
Player.load_sprites()

# SPRITE IMAGES
background = desert_sprite.subsurface(pygame.Rect((14, 76), (50, 56)))
rock = desert_sprite.subsurface(pygame.Rect((170, 230), (35, 35)))
cactus = cacti_sprites.subsurface(pygame.Rect((0, 0), (38, 50))).convert_alpha()

# SNAKE ITEMS
Snake_Class.snake.screen = screen  # feeds the screen variable to the snake instance in Snake_Class
DK_BROWN = (116, 71, 48)


def update(point, goal):
	"""
	This functon takes in two parameters, each of which is a two tuple
	list representing a point on the screen.

	The function returns the direction the point needs to move in in
	order to be closer to the gaol.

	The direction is returned as a point_x_speed, and a point_y_speed
	"""
	point_x_speed = 0
	point_y_speed = 0
	if (point[0] < goal[0]) and (point[1] < goal[1]):
		point_x_speed += tile_size
		point_y_speed += tile_size
	elif (point[0] < goal[0]) and (point[1] > goal[1]):
		point_x_speed += tile_size
		point_y_speed -= tile_size
	elif (point[0] > goal[0]) and (point[1] > goal[1]):
		point_x_speed -= tile_size
		point_y_speed -= tile_size
	elif point[0] > goal[0] and point[1] < goal[1]:
		point_x_speed -= tile_size
		point_y_speed += tile_size
	elif point[0] < goal[0]:
		point_x_speed += tile_size
	elif point[0] > goal[0]:
		point_x_speed -= tile_size
	elif point[1] < goal[1]:
		point_y_speed += tile_size
	elif point[1] > goal[1]:
		point_y_speed -= tile_size

	return [point_x_speed, point_y_speed]


def distance(point1, point2):
	"""
	Returns the distance between two points.

	"""
	distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
	return distance

"""
The section below creates the first goal for the snake.
The list of babies is searched for the baby that is closest to the snake.
Then, a path is found to that baby
"""

for item in babyStarts:
	Snake_Class.snake.goal_list.append(item)

goal_grid = Snake_Class.snake.getDistance(babyStarts)
Snake_Class.snake.getGoalGrid(goal_grid)

snake_agent = pathfinder.newAgent([Snake_Class.snake.A[0] / tile_size, (Snake_Class.snake.A[1] + 50) / tile_size],
								  goal_grid)
snake_path = snake_agent.getPath(board)

index = 1 # Used to access item in the snake_path list

# PLAY THE GAME
while True:

	# GET EVENTS FROM THE USER
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		# IF THE EVENT TYPE IS A KEYDOWN AND THE PLAYER RENDERING HAS COMPLETED...
		if event.type == pygame.KEYDOWN and player.updated:
			# LOOK FOR A VALID EVENT FROM THE USER
			player.next_x = 0
			player.next_y = 0
			# IF THE KEYDOWN IS A MOVEMENT KEY, MAKE SURE THE USER ISN'T TRYING TO GO INTO AN OBSTACLE
			if event.key == pygame.K_LEFT:
				if not [player.x - 1, player.y] in obstacles:
					player.next_x = -1
					player.direction = player.LEFT
			elif event.key == pygame.K_RIGHT:
				if not [player.x + 1, player.y] in obstacles:
					player.next_x = 1
					player.direction = player.RIGHT
			elif event.key == pygame.K_UP:
				if not [player.x, player.y - 1] in obstacles:
					player.next_y = -1
					player.direction = player.UP
			elif event.key == pygame.K_DOWN:
				if not [player.x, player.y + 1] in obstacles:
					player.next_y = 1
					player.direction = player.DOWN
			# IF THE EVENT KEYDOWN IS A SPACE, LOOK FOR A MONGOOSE TO BE RESCUED AT THE CURRENT PLAYER LOCATION
			elif event.key == pygame.K_SPACE:
				if [player.x, player.y] in babyStarts:
					print "You have rescued a baby mongoose!"  # TODO: Increment "babies saved" variable
					for i in range(len(babyStarts)):
						if babyStarts[i] == [player.x, player.y]:
							babyStarts.pop(i)
							babies.pop(i)
							break
			# VERIFY MOVEMENT DOES NOT GO OFF THE BOARD, IF SO, DELETE MOVE EVENT
			if player.x < 0 or player.x >= board.width:
				player.updated = True
			if player.y < 0 or player.y >= board.height:
				player.updated = True
			# IF A MOVEMENT KEYDOWN WAS FOUND, SET THE PLAYER RENDERING TO INCOMPLETE
			if player.next_y != 0 or player.next_x != 0:
				player.update_pixel_coordinates(tile_size)
				player.updated = False

	# DRAW THE DESERT BACKGROUND
	for i in range(board.width):
		xStart = i * 50
		for j in range(board.height):
			yStart = zoneHeight + j * 56
			screen.blit(background, (xStart, yStart))

	# DRAW THE ROCK OBSTACLES
	for r in rocks:
		screen.blit(rock, (r[0] * tile_size, zoneHeight + r[1] * tile_size))

	# DRAW THE CACTI
	for cact in cacti:
		# -3 and -15 below are for improved graphics based on the difference
		# between tile_size and the size of the cactus image
		screen.blit(cactus, (cact[0] * tile_size - 3, zoneHeight + cact[1] * tile_size - 15))

	# DRAW THE TOP BORDER ON THE SCREEN
	pygame.draw.rect(screen, colors['bufferZone'], (0, 0, board.width * tile_size, zoneHeight), 10)
	pygame.draw.rect(screen, colors['bufferFill'], (10, 10, board.width * tile_size - 20, zoneHeight - 10))

	# DRAW THE BABIES BASED ON THEIR PROXIMITY TO THE SNAKE
	for baby in babies:
		# distance = distance(snake.A, [baby.x * tile_size, baby.y * tile_size])
		# if 75 < distance <= 150:
		# baby.currentState = Baby.scared
		# elif distance <= 75:
		# baby.currentState = Baby.veryScared
		# else:
		# 	baby.currentState = Baby.stoic
		baby.currentState = Baby.stoic  # TODO: Delete this line when the above commented out code works
		screen.blit(baby.updateRendering(deltaTime), (baby.x * tile_size + 5, zoneHeight + baby.y * tile_size + 5))

	# DRAW THE PLAYER BASED ON RENDERING BEING COMPLETE OR INCOMPLETE
	# IF INCOMPLETE, UPDATE THE START LOCATION OF THE SPRITE RECT BASED ON THE PLAYER DIRECTION AND REEVALUATE COMPLETE
	if not player.updated:  # or [player.pixX / tile_size, player.pixY / tile_size] not in obstacles:
		screen.blit(player.updateRendering(deltaTime), (player.pixX, player.pixY + zoneHeight - 10))
		if player.next_x > 0:
			player.pixX += horizontal_speed * player.next_x
			if player.pixX / tile_size != player.x:
				player.x += player.next_x
				player.direction = player.STILL
				player.updated = True
		elif player.next_x < 0:
			player.pixX += horizontal_speed * player.next_x
			if player.pixX / tile_size < player.x - 1:
				player.x += player.next_x
				player.direction = player.STILL
				player.updated = True
		elif player.next_y > 0:
			player.pixY += vertical_speed * player.next_y
			if player.pixY / tile_size != player.y:
				player.y += player.next_y
				player.direction = player.STILL
				player.updated = True
		elif player.next_y < 0:
			player.pixY += vertical_speed * player.next_y
			if player.pixY / tile_size < player.y - 1:
				player.y += player.next_y
				player.direction = player.STILL
				player.updated = True
	# IF THE RENDERING IS COMPLETE, DRAW THE PLAYER LOOKING FORWARD (STOIC)
	else:
		screen.blit(player.updateRendering(deltaTime), (player.x * tile_size, player.y * tile_size + zoneHeight - 10))

	# SNAKE ITEMS
	"""
	The if Statement below will measure the distance between A and the goal and set the X-speed and
	Y-speed accordingly.

	Next it will take the next item in the snake's A-Star path and multiply each element by 25 to
	convert the element to a pixel on the screen.

	Finally the index is incremented.
	"""
	if distance(Snake_Class.snake.A, Snake_Class.snake.goal) >= 70:
		if index <= len(snake_path):
			Snake_Class.snake.point_x_speed = update(Snake_Class.snake.A, Snake_Class.snake.goal)[0]
			Snake_Class.snake.point_y_speed = update(Snake_Class.snake.A, Snake_Class.snake.goal)[1]
			Snake_Class.snake.A = [snake_path[index - 1][0] * tile_size, (snake_path[index - 1][1] * tile_size) + 50]
			index += 1

	# transition triggers
	if distance(Snake_Class.snake.A, ((Snake_Class.snake.goal[0]), (Snake_Class.snake.goal[1]))) < 150:
		"""
		if the snake is not already in Offense State, switch to an offensive State
		"""
		if Snake_Class.snake.FSM.cur_state_name != "Offense":
			Snake_Class.snake.FSM.Transition("To_Offense")
			Snake_Class.snake.FSM.Traveling = False
			Snake_Class.snake.FSM.Attack = False
			print "Nag is Offensive"

		if Snake_Class.snake.FSM.cur_state_name == "Offense":
			if Snake_Class.timer.delta_time_Attack(10000):
				Snake_Class.snake.FSM.Transition("To_Attack")
				Snake_Class.snake.FSM.Traveling = False
				Snake_Class.snake.FSM.Attack = False
				print "Nag is Attacking!!!!"
				if Snake_Class.snake.collision():
					Snake_Class.snake.FSM.Transition("To_Traveling")
					Snake_Class.snake.FSM.Offense = False
					Snake_Class.snake.FSM.Attack = False

					for i in range(len(babyStarts)):
						if babyStarts[i] == goal_grid:
							babyStarts.pop(i)
							babies.pop(i)
							break
					if len(babies) == 0:
						print "The game is finished"
						pygame.quit()
						sys.exit()
					goal_grid = Snake_Class.snake.getDistance(babyStarts)
					Snake_Class.snake.getGoalGrid(goal_grid)
					snake_agent = pathfinder.newAgent([Snake_Class.snake.A[0] / tile_size,
													   Snake_Class.snake.A[1] / tile_size], goal_grid)
					snake_path = snake_agent.getPath(board)
					index = 1
		Snake_Class.snake.FSM.Execute()

	else:
		if Snake_Class.snake.FSM.cur_state_name != "Traveling":
			Snake_Class.snake.FSM.Transition("To_Traveling")
			Snake_Class.snake.FSM.Offense = False
			Snake_Class.snake.FSM.Attack = False
			index = 1
			print "Nag is Traveling"

		"""
		if len(C_snake_path) == 0:
			if line_of_sight((Snake_Class.snake.A[0] / tile_size, (Snake_Class.snake.A[1] / tile_size)), (Snake_Class.snake.C[0] / tile_size, (Snake_Class.snake.C[1] / tile_size))) == True:
				Cmove = True
				Atemp = (Snake_Class.snake.A[0] / tile_size, (Snake_Class.snake.A[1] / tile_size))
				C_snake_agent = pathfinder.newAgent([Snake_Class.snake.C[0]/ tile_size, Snake_Class.snake.C[1]/ tile_size], goal_grid)
				C_snake_path = C_snake_agent.getPath(board)
		"""
		Snake_Class.snake.FSM.Execute()

	Snake_Class.snake.head_circle = pygame.Rect(Snake_Class.snake.A[0] - 40,
												Snake_Class.snake.A[1] - 40, 40 * 2, 40 * 2)

	# INCREMENT DELTATIME, USED FOR CHOOSING WHICH SPRITE TO RENDER TO THE SCREEN FOR BABY AND PLAYER OBJECTS
	deltaTime += 1

	# SET THE FRAMERATE AND UPDATE THE SCREEN
	clock.tick(5)
	pygame.display.flip()

pygame.quit()
sys.exit()