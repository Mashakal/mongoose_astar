"""
Created on:  March 17, 2015
Created by:  Alex Neuenkirk
"""
import pygame

UPDATESPEED = 0


class Player():
	rescuing = 1
	paralyzed = 0
	UP = "UP"
	DOWN = "DOWN"
	LEFT = "LEFT"
	RIGHT = "RIGHT"
	NONE = "NONE"
	STILL = "STILL"

	def __init__(self, pos, deltaTime=0):
		"""
		Constructor for the Player class.
		:param pos: the tile location to start the player, [column, row]
		:param deltaTime: the number of frames since the game started, defaults to 0 if omitted.
		:return: void
		"""
		self.x = pos[0]  # Holds the player's column position
		self.y = pos[1]  # Holds the player's row position
		self.currentState = self.rescuing
		self.lastUpdateTime = deltaTime  # Tells us how long since the last sprite update
		self.spriteIndex = 0  # Tells us which sprite in a spriteSet list to send to the game loop for rendering
		self.spriteTransitioner = 1  # Increments the spriteIndex variable
		self.updated = True  # Used allow user input or not
		self.direction = self.NONE  # The direction the player is facing or moving
		self.next_x = 0  # The next column increment value based on user keydown input
		self.next_y = 0  # The next row increment value based on user keydown input
		self.pixX = 0  # The x-value pixel location of the player
		self.pixY = 0  # The y-value pixel location of the player

	def update_pixel_coordinates(self, tile_size):
		"""
		Updates the pixel location of the player based on its tile location.
		:param tile_size: the size of the tiles in pixels
		:return:  void
		"""
		self.pixX = self.x * tile_size
		self.pixY = self.y * tile_size

	def updateRendering(self, deltaTime):
		"""
		Provides the next player sprite to be rendered to the screen.
		:param: deltaTime: the number of frames passed since the start of the game
		:return: the applicable sprite to be rendered for the player display
		"""
		spriteSet = []
		if self.currentState == self.rescuing:
			if self.direction == self.UP:
				spriteSet = Player.upSprites
			elif self.direction == self.DOWN:
				spriteSet = Player.downSprites
			elif self.direction == self.RIGHT:
				spriteSet = Player.rightSprites
			elif self.direction == self.LEFT:
				spriteSet = Player.leftSprites
			else:
				spriteSet = Player.forwardSprites
		elif self.currentState == self.paralyzed:
			spriteSet = Player.paralyzedSprites

		if deltaTime - self.lastUpdateTime > UPDATESPEED:
			if self.spriteIndex >= len(spriteSet) - 1:
				self.spriteIndex = -1
			elif self.spriteIndex == 0:
				self.spriteTransitioner = 1
			self.spriteIndex += self.spriteTransitioner
			self.lastUpdateTime = deltaTime

		# print spriteSet
		return spriteSet[self.spriteIndex]

	@staticmethod
	def load_sprites():
		"""
		Loads the sprites needed to render the player to the board.
		:return: void
		"""
		player_spritesheet = pygame.image.load("ash.png").convert_alpha()

		# Forward facing
		f0 = player_spritesheet.subsurface(pygame.Rect((43, 324), (35, 45)))
		f1 = player_spritesheet.subsurface(pygame.Rect((75, 324), (35, 45)))
		f2 = player_spritesheet.subsurface(pygame.Rect((138, 324), (30, 45)))
		Player.forwardSprites = [f0, f1, f2, f1, f0]

		# Moving right
		r1 = player_spritesheet.subsurface(pygame.Rect((43, 565), (40, 45)))
		r2 = player_spritesheet.subsurface(pygame.Rect((84, 564), (40, 45)))
		r3 = player_spritesheet.subsurface(pygame.Rect((126, 564), (40, 45)))
		r4 = player_spritesheet.subsurface(pygame.Rect((179, 565), (40, 45)))
		r5 = player_spritesheet.subsurface(pygame.Rect((228, 565), (40, 45)))
		r6 = player_spritesheet.subsurface(pygame.Rect((268, 565), (40, 45)))
		r7 = player_spritesheet.subsurface(pygame.Rect((310, 565), (40, 45)))
		r8 = player_spritesheet.subsurface(pygame.Rect((366, 567), (40, 45)))
		Player.rightSprites = [r1, r2, r3, r4, r5, r6, r7, r8]

		# Moving left
		l1 = player_spritesheet.subsurface(pygame.Rect((372, 633), (40, 45)))
		l2 = player_spritesheet.subsurface(pygame.Rect((331, 632), (40, 45)))
		l3 = player_spritesheet.subsurface(pygame.Rect((284, 632), (40, 45)))
		l4 = player_spritesheet.subsurface(pygame.Rect((232, 633), (40, 45)))
		l5 = player_spritesheet.subsurface(pygame.Rect((185, 633), (40, 45)))
		l6 = player_spritesheet.subsurface(pygame.Rect((147, 633), (40, 45)))
		l7 = player_spritesheet.subsurface(pygame.Rect((100, 633), (40, 45)))
		l8 = player_spritesheet.subsurface(pygame.Rect((43, 635), (40, 45)))
		Player.leftSprites = [l1, l2, l3, l4, l5, l6, l7, l8]

		# Moving up
		u1 = player_spritesheet.subsurface(pygame.Rect((155, 407), (35, 50)))  # both feet level
		u2 = player_spritesheet.subsurface(pygame.Rect((189, 407), (35, 50)))  # right foot up
		u3 = player_spritesheet.subsurface(pygame.Rect((225, 407), (35, 50)))  # left foot up
		Player.upSprites = [u1, u2, u1, u3]

		# Moving down
		d1 = player_spritesheet.subsurface(pygame.Rect((33, 406), (35, 51)))
		d2 = player_spritesheet.subsurface(pygame.Rect((72, 406), (35, 51)))
		Player.downSprites = [d1, d2]

		# Paralyzed
		p1 = player_spritesheet.subsurface(pygame.Rect((338, 179), (35, 45)))
		Player.paralyzedSprites = [p1]