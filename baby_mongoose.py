"""
Created on:  March 7, 2015
Created by:  Alex Neuenkirk
"""
import pygame
import random


class Baby():
	stoic = 1
	scared = -1
	veryScared = -2
	seeking = 5
	dead = 0
	spawnLocations = [[1, 0], [10, 0], [5, 6], [33, 5], [27, 12], [17, 13]]
	currentLocations = []

	def __init__(self, pos, deltaTime=0):
		"""
        Constructor for the baby mongoose class for the Mongoose game.
        :param tileX: the x-coordinate for the tile position to render the baby
        :param tileY: the y-coordinate for the tile position to render the baby
        :return:
        """
		self.x = pos[0]
		self.y = pos[1]
		self.currentState = self.stoic
		self.birthTime = deltaTime
		self.lastUpdateTime = deltaTime
		self.spriteIndex = 0
		self.spriteTransitioner = 1

	def updateRendering(self, deltaTime):
		"""
        Updates the sprite data for the baby mongoose based on frames.
        :rtype : sprite subsurface for current frameset
        :param deltaTime: The change in frames since the game began running.
        :return: the updated sprite to be used for rendering the baby mongoose.
        """
		spriteSet = []
		if self.currentState == self.stoic:
			spriteSet = Baby.stoicSprites
		elif self.currentState == self.scared:
			spriteSet = Baby.scaredSprites
		elif self.currentState == self.veryScared:
			spriteSet = Baby.veryScaredSprites

		if deltaTime - self.lastUpdateTime > random.randint(2, 15):
			if self.spriteIndex >= len(spriteSet) - 1:
				self.spriteTransitioner = -1
			elif self.spriteIndex == 0:
				self.spriteTransitioner = 1
			self.spriteIndex += self.spriteTransitioner
			self.lastUpdateTime = deltaTime
		return spriteSet[self.spriteIndex]

	@staticmethod
	def load_sprites():
		"""
        Loads the sprites needed to portray a baby on the board.
        """
		baby_spritesheet = pygame.image.load("babies.png").convert_alpha()

		# Stoic sprites
		'''
		These are Hamtaro sprites:
		n0 = baby_spritesheet.subsurface(pygame.Rect((4, 1153), (45, 45)))  # facing front
		n1 = baby_spritesheet.subsurface(pygame.Rect((2, 1037), (43, 50)))  # turned right
		n2 = baby_spritesheet.subsurface(pygame.Rect((52, 1153), (45, 45)))  # facing front and squinting
		n3 = baby_spritesheet.subsurface(pygame.Rect((309, 1037), (42, 50)))  # turned left
		'''
		n0 = baby_spritesheet.subsurface(pygame.Rect((183, 428), (23, 24)))
		n1 = baby_spritesheet.subsurface(pygame.Rect((206, 428), (23, 24)))
		n2 = baby_spritesheet.subsurface(pygame.Rect((229, 428), (23, 24)))
		n3 = baby_spritesheet.subsurface(pygame.Rect((252, 428), (23, 24)))
		n4 = baby_spritesheet.subsurface(pygame.Rect((275, 428), (23, 24)))
		Baby.stoicSprites = [n0, n1, n2, n3, n4]

		# Scared sprites
		s1 = baby_spritesheet.subsurface(pygame.Rect((395, 2245), (49, 43)))
		s2 = baby_spritesheet.subsurface(pygame.Rect((443, 2245), (47, 43)))
		s3 = baby_spritesheet.subsurface(pygame.Rect((491, 2245), (47, 44)))
		s4 = baby_spritesheet.subsurface(pygame.Rect((587, 2245), (47, 44)))
		s5 = baby_spritesheet.subsurface(pygame.Rect((587, 2245), (47, 44)))
		s6 = baby_spritesheet.subsurface(pygame.Rect((635, 2245), (47, 44)))
		Baby.scaredSprites = [s1, s2, s3, s1, s4, s5, s6]

		# Very scared sprites
		v1 = baby_spritesheet.subsurface(pygame.Rect((110, 715), (47, 44)))
		v2 = baby_spritesheet.subsurface(pygame.Rect((166, 715), (47, 44)))
		v3 = baby_spritesheet.subsurface(pygame.Rect((218, 715), (47, 44)))
		v4 = baby_spritesheet.subsurface(pygame.Rect((268, 715), (47, 44)))
		Baby.veryScaredSprites = [v1, v2, v3, v4]