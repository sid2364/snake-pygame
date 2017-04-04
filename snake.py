'''
To play the game: python game.py
Packaged using cx_Freeze maintained by Anthony Tuininga (anthony.tuininga@gmail.com): python setup.py build
'''

import pygame
import random
import time
import math


title = "Snake"
resolution = [800, 600]
background = (50, 65, 50) # blackish-green
white = (255, 255, 255)
snake = (50, 150, 80) # the snake
food = (240, 50, 0) # and red apple
FPS = 40 # tick rate
change = 5 # "difficulty level"
scoreFile = "score.dat"

# init pygame stuff
pygame.init()
gameDisplay = pygame.display.set_mode(resolution)
gameDisplay.fill(background)
pygame.display.set_caption(title)
pygame.display.update()
clock = pygame.time.Clock()

# this "hack" is for maintaining direction of snake
# i.e. you can't just turn around
goingDir = {0: pygame.K_UP, 1: pygame.K_RIGHT, 2: pygame.K_DOWN, 3: pygame.K_LEFT}
mapDir = {pygame.K_UP: 0, pygame.K_RIGHT: 1, pygame.K_DOWN: 2, pygame.K_LEFT: 3}
font = pygame.font.SysFont(None, 40)
block = 10
beatHighScore = False

# create file if it doesn't exist, read from it if it does
try:
	fp = open(scoreFile, "r")
	newHighScore = oldHighScore = int(fp.read())
except IOError, e:
	fp = open(scoreFile, "w")
	newHighScore = oldHighScore = 0

# pass param to write, else read
def rwHighScore(scoreToWrite=0):
	if scoreToWrite != 0:
		with open(scoreFile, "w") as score:
			score.write("%d" % (scoreToWrite))
			return 0 # value isn't used
	else:
		for l in open(scoreFile, "r+"):
			if l.strip():
				return int(l)
		else:
			return 0

def displayMessage(message, color=(255, 255, 255), where=[resolution[0]/2-200, resolution[1]/2-200]):
	screenText = font.render(message, True, color)
	gameDisplay.blit(screenText, where)

def randomFoodGen():
	return random.randrange(10,resolution[0]-10, 5), random.randrange(10,resolution[1]-10, 5)

def setDifficulty():
	gameDisplay.fill(background)

	displayMessage("Choose difficulty level:-",\
			snake, [resolution[0]/2-200, resolution[1]/2 - 150])
	displayMessage("1 - I'm a n00b, go easy on me!",\
			snake, [resolution[0]/2-200, resolution[1]/2 - 30])
	displayMessage("2 - Bring it on!", \
			snake,[resolution[0]/2-200, resolution[1]/2])
	displayMessage("3 - I can do this with my eyes closed!", \
			snake, [resolution[0]/2-200, resolution[1]/2 + 30])
	displayMessage("Q - Get me out of here already!", \
			snake, [resolution[0]/2-200, resolution[1]/2 + 90])
	pygame.display.update()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
					return 0
				if event.key == pygame.K_1:
					return 2
				if event.key == pygame.K_2:
					return 5
				if event.key == pygame.K_3:
					return 10

# "pause" gameplay - hide snake, food, and score
def goToSleep(snakeList, lead_x, lead_y, score, snakeLength, gamePlay):
	# drawSnake(snakeList, lead_x, lead_y, score, snakeLength, gamePlay) # don't draw anything!
	gameDisplay.fill(background)
	displayMessage("Press 'Q' to exit to main menu or 'R' to resume the game", white, (0, resolution[1]-30))
	pygame.display.update()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.exit()
				exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
					return True
				if event.key == pygame.K_r:
						return False

# snakeList contains current positions of the snake 
# lead_x, _y are the where he's moving into now
def drawSnake(snakeList, lead_x, lead_y, score, snakeLength, gamePlay):
	
	global newHighScore
	global beatHighScore
	
	gameDisplay.fill(background)
	
	snakeHead = []
	snakeHead.append(lead_x)
	snakeHead.append(lead_y)
	snakeList.append(snakeHead)
	if len(snakeList)*1.5 > snakeLength:
		del snakeList[0]
	
	for xy in snakeList:
		pygame.draw.rect(gameDisplay, snake, [xy[0], xy[1], block, block]) # snake

	if len(snakeList) > 2:
		for part in snakeList[:-1]:
			if part == snakeHead:
				return False # gamePlay

	if oldHighScore < score:
		beatHighScore = True
		beaten = "You have beaten the high score!"
		newHighScore = score
	else:
		beaten = "Keep playing!"
	displayMessage("Score: %d - High Score: %d %s" % (score, oldHighScore, beaten), white, (0,0))
	
	return gamePlay # return this as is

# main game loop
def gameLoop():
	global change
	global oldHighScore

	change = setDifficulty()
	if change == 0: # 0 is is they selected "Q"
		return False
	lead_x_delta = change
	lead_y_delta = 0
	snakeLength = 10
	snakeList = [[resolution[0]/2 + x, resolution[1]/2] for x in range(0, snakeLength*change, change)]
	lead_x = snakeList[len(snakeList)-1][0]
	lead_y = snakeList[len(snakeList)-1][1]
	appleX, appleY = randomFoodGen()
	gamePlay = True
	score = 0
	direction = mapDir[pygame.K_RIGHT] # starting direction
	
	gameDisplay.fill(background)
	
	while gamePlay: # main game loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
					gamePlay = False
				# don't let him turn around and update the new direction
				if event.key == pygame.K_LEFT and event.key != goingDir[(direction+2)%4]:
					lead_x_delta = -change
					lead_y_delta = 0
					direction = mapDir[event.key]
				elif event.key == pygame.K_RIGHT and event.key != goingDir[(direction+2)%4]:
					lead_x_delta = change
					lead_y_delta = 0
					direction = mapDir[event.key]
				elif event.key == pygame.K_UP and event.key != goingDir[(direction+2)%4]:
					lead_x_delta = 0
					lead_y_delta = -change
					direction = mapDir[event.key]
				elif event.key == pygame.K_DOWN and event.key != goingDir[(direction+2)%4]:
					lead_x_delta = 0
					lead_y_delta = change
					direction = mapDir[event.key]
				# "pause"
				elif event.key == pygame.K_p:
					if goToSleep(snakeList, lead_x, lead_y, score, snakeLength, gamePlay):
						return True
		lead_x += lead_x_delta
		lead_y += lead_y_delta
	
		lead_x %= resolution[0]-block/2
		lead_y %= resolution[1]-block/2
		
		# snake got the apple? (why are snakes eating apples?)
		# increase length, score, and put out more food
		if abs(lead_x - appleX) < 10 and abs(lead_y - appleY) < 10:
			appleX, appleY = randomFoodGen()
			score += change
			snakeLength += change*(3/math.log(change))

		gamePlay = drawSnake(snakeList, lead_x, lead_y, score, snakeLength, gamePlay)
		pygame.draw.rect(gameDisplay, food, [appleX, appleY, 10, 10]) # draw food
		displayMessage("Press 'Q' to exit to main menu or 'P' to pause the game", white, (0, resolution[1]-30))
		pygame.display.update() # update after every event
		clock.tick(FPS)

	while not gamePlay:
		gameDisplay.fill(background)
		displayMessage("Press 'S' to start game again or 'Q' to quit!",\
			 snake, [resolution[0]/2-280, resolution[1]/2-200])
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
					return False
				if event.key == pygame.K_s:
					oldHighScore = newHighScore
					return True


if __name__ == "__main__":

	displayMessage("Welcome to Snake!", white, [resolution[0]/2-120, resolution[1]/2])
	pygame.display.update()
	time.sleep(1)
	# if gameLoop() returns False then don't start another
	# it will return False when you pressed 'Q' not when GAME OVER
	while gameLoop():
		gameDisplay.fill(background)
		gameLoop()
	gameDisplay.fill(background)
	displayMessage("Good bye!",\
		white, [resolution[0]/2-70, resolution[1]/2])
	
	# update the high score if a new record was made
	if beatHighScore:
		rwHighScore(newHighScore)
		displayMessage("Congratulations on beating the high score!",\
			white, [resolution[0]/2 - 270, resolution[1]/2 - 40])

		pygame.display.update()
		time.sleep(3)
	pygame.display.update()
	pygame.quit()
	quit()

