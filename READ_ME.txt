#######################################
              MONGOOSE
#######################################
Created by:
Alex Neuenkirk
Ren C'deBaca

---------------------------------------------------
Mongoose is an arcade game that implements key concepts 
of AI in a fun and aesthetic platform. 

The object of the game is to collect all of the Baby
mongooses before the evil snake, Nag, gobbles them
up first!!!


Build Instructions
---------------------------------------------------
Executing the Mongoose file will start the game.



Game Instructions
---------------------------------------------------
Use the arrow keys to move.
Collect Babies by passing over them and pressing the space bar.



Basic Game Structure
--------------------------------------------------
The game Mongoose is a grid based game. 

A* is used over this grid to navigate the snake to its goals (The babies).
The behavior of the snake is controled a finite state machine. 



Discription of Modules
---------------------------------------------------
***
MONGOOSE.PY:
	Contains the main game loop and variables nessasary for the inital construction of the game.

  Imports:
	sys
	pathfindAstar as pathfinder
	pygame
	random
	pygame.locals
	math
	Snake_Class
	Vector_Class
	baby_mongoose import Baby
	mongoose_player import player
	

  Main Game Setup:
	-creates colors
	-Sets up the board with tile_size, and gets the width and Height of the board 
	-Initializes Pygame, the game clock, and the window
	-Loads the images used for the obsticals
	-creates subsurfaces to carry the obstical images 
	-Generates the Baby Mongooses' starting postions and creates objects of type Baby with those starting positons
	-Finds the Closest baby to the snake and generates an A* path to the baby

  Game Loop:
	-Check if the user has Quit
	-Check if keys are being pressed and update player movment
	-Draw Player 
	-Draw the Game Backgroups
	-Draw the Obsticals
	-Draw the Cacti
	-Draw the Babies
	-Draw the Bufferzone at Top of the screen

	-Snake Movement:
		-If Snake is far from goal -> move snake along A* path

	-Snake Finite State Machine Triggers:
		-If snake is far from goal -> snake should be in the "Traveling" state
		-If snake is close to goal -> snake should be in the "Offensive" state
		-If snake has been offensive for 4 seconds -> snake should be in "Attack" state  

	-Draw the snake
	-Increment the deltaTime variable 
	-Clock tick
	-Update the screen 

***
PATHFINDASTAR.PY:
	Contains the classes and functions that are essential in an A* search used for our Mongoose game. 

  imports:
	math
	random

  Contains the Classes:
	-newAgent()
		-Used for creating and agent object and getting a path to its goals.
	-PathfindingList()
		-Used for maintaining the open and closed lists used in our A* search.
	-Board()
		-Holds important information about the gambe board and has an important method, getConnections().
	-TileRecord()
		-Used to save tile information for the frontier and the previously visited tiles.

***
BABY_MONGOOSE.PY:
	Contains the class that manages the baby mongooses. 

  imports:
	pygame

  Contains the Class:
	-Baby()
		-Controls the Baby agent information and holds their sprites

***
Snake_Class:
	Contains the Classes that create the snake's image as well as holds the 
	snake's atributes. The instance of snake is also created in this class. 

  imports:
	math
	Vector_Class
	pygame
	SnakeFSM 

  Contains the Classes:
	-Snake_Body()
		- creates the individual benzier curves that consponse the snake's body 
	-Snake()
		-creates the snake and holds infomation about the snake's location and states
	-Timer()
		-used to time when the Attack substate should be triggered 

  Contains the Instance:
	-snake --> main antagonist in the Game 

***
SnakeFSM:
	Creates the structer of the snake's FSM. The snake's movments are percribed by 
	parameters and functions within each of these states 

  imports:
	Vector_Class
	math 

  Contains the Classes: 
	-Taveling()
		- Contains movment details for when the snake is moving from point to point (
	-Offense()
		- moves the snake into offesnive positions based upon the location of the goal and 
		the direction the snake is appoching from
	-Attack()
		- spings the snake's head forward for a fatal blow. check of collision 
	-Transition()
		- used to ensure states stansition smoothly 
	-SnakeFSM()
		- Contains dictionaries that decalre the snake's possible states and functions for
		navigating these dictonaries 

***
Vector_Class:
	Holds the class Vector that creates a vector out of two points and provides 
	a function that can preform vector addition on two Vector objects 

  Contains the Class:
	-Vector()












