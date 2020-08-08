import pygame
import random
import math
import sys
from pygame import mixer

# -- CONSTANT VARIABLES --
WN_LENGTH = 600
WN_HEIGHT = 800
NUM_OF_SQUARES = 30
SQ_LEN = WN_LENGTH // NUM_OF_SQUARES
# 	- snake and food -
RED = (146, 36, 40)
YELLOW = (218, 124, 48)
# 	- forest colors -
GREEN = (63, 128, 70)
DARK_GREEN = (0, 82, 33)
# 	- outline and background
BLACK = (0, 0, 0)

WN = pygame.display.set_mode( (WN_LENGTH, WN_HEIGHT) )
TITLE = pygame.display.set_caption("Hungry Hungry Snake!")
CLOCK = pygame.time.Clock()


class Snake:
	def __init__(self):
		# Snake body = array as large as number of squares
		# on the screen (in case snake is as big as screen)
		self.x = [WN_LENGTH//2]
		self.y = [WN_LENGTH//2]
		for i in range(0, SQ_LEN*SQ_LEN):
			self.x.append(-100)
			self.y.append(-100)
		self.x_change = 0
		self.y_change = 0
		self.length = 1

	# Checks if snake has reached the boundary of the grid
	def at_boundary(self):
		# First check if snake has hit itself
		for i in range(self.length, 1, -1):
			if self.x[0] == self.x[i] and self.y[0] == self.y[i]:
				return True
		return self.x[0] <= 0 or self.x[0] >= (WN_LENGTH-SQ_LEN) or self.y[0] <= 200 or self.y[0] >= (WN_HEIGHT-SQ_LEN)

	def move_up(self):
		self.y_change = -SQ_LEN
		self.x_change = 0

	def move_left(self):
		self.y_change = 0
		self.x_change = -SQ_LEN

	def move_down(self):
		self.y_change = SQ_LEN
		self.x_change = 0

	def move_right(self):
		self.y_change = 0
		self.x_change = SQ_LEN

	# Draw snake with red square and a black border
	def drawSnake(self):
		for i in range(self.length):
			pygame.draw.rect(WN, RED, (self.x[i], self.y[i], SQ_LEN, SQ_LEN), False)
			pygame.draw.rect(WN, BLACK, (self.x[i], self.y[i], SQ_LEN, SQ_LEN), True)

	def updateSnake(self, color=RED):
		# updates how long the snake is by making current length
		# equal to the previous length 
		for i in range(self.length, 0, -1):
			self.x[i] = self.x[i-1]
			self.y[i] = self.y[i-1]
		if not self.at_boundary():
			self.x[0] += self.x_change
			self.y[0] += self.y_change
		else:
			game_over(self.length - 1)
			sys.exit()
		self.drawSnake()


class Food:
	def __init__(self):
		self.size = SQ_LEN
		# Formula to keep the food on the screen during every generation
		self.x = (random.randint(2, NUM_OF_SQUARES - 1) * SQ_LEN) - SQ_LEN
		self.y = 200 + (random.randint(2, NUM_OF_SQUARES - 1) * SQ_LEN) - SQ_LEN

	# Draw food with yellow square and black border
	def updateFood(self):
		pygame.draw.rect(WN, YELLOW, (self.x, self.y, self.size, self.size))
		pygame.draw.rect(WN, BLACK, (self.x, self.y, self.size, self.size), True)


def is_ate(snake, food):
	return snake.x[0] == food.x and snake.y[0] == food.y

def eat_sound():
	chomp = mixer.Sound('food_ate.wav')
	chomp.play()

# Draws the grid, as well as updates the food and snake with each call
def updateGrid(score, snake, food):
	for row in range(NUM_OF_SQUARES):
		for col in range(NUM_OF_SQUARES):
			color = GREEN
			# if at the border of grid, color dark green
			# else, color regular green
			if row == 0 or row == NUM_OF_SQUARES - 1 or col == 0 or col == NUM_OF_SQUARES - 1:
				color = DARK_GREEN
				pygame.draw.rect(WN, color, (0 + SQ_LEN*col, 200 + SQ_LEN*row, SQ_LEN, SQ_LEN), False )
				pygame.draw.rect(WN, BLACK, (0 + SQ_LEN*col, 200 + SQ_LEN*row, SQ_LEN, SQ_LEN), True )
			else:
				pygame.draw.rect(WN, color, (0 + SQ_LEN*col, 200 + SQ_LEN*row, SQ_LEN, SQ_LEN), False )
	food.updateFood()
	snake.updateSnake()
	# (170, 70) --> x and y of where the score will be placed on the screen
	displayScore(score, 170, 70)
	pygame.display.update()

def displayScore(score, x, y):
	text = pygame.font.SysFont("arial", 100)
	score = text.render(f'Score: {score}', 1, YELLOW)
	WN.blit(score, (x, y))

# Displays the game over screen, and asks the user if the user 
# wants to play again or quit
def game_over(score):
	text = pygame.font.SysFont("arial", 100)
	gameOver = text.render(f'Game Over!', 1, YELLOW)
	subText = pygame.font.SysFont("arial", 50)
	playAgain = subText.render('Play Again: Space', 1, GREEN)
	endGame = subText.render('Close: Any key', 1, RED)

	WN.fill(BLACK)
	displayScore(score, 100, 280)
	WN.blit(gameOver, (100, 200))
	WN.blit(playAgain, (100, 550))
	WN.blit(endGame, (100, 600))
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			# user can hit the x to close if they want
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				# space - restart execution
				if event.key == pygame.K_SPACE:
					play_game()
				# any other key - exit
				else:
					sys.exit()

def pause(score):
	paused = True
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				paused = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					paused = False

# Main game function
def play_game():
	snake = Snake()
	food = Food()
	score = 0
	# load in and play music
	background = 'stolenDance.wav'
	pygame.mixer.music.load(background)
	pygame.mixer.music.play()

	running = True
	while running:
		WN.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				# moves the snake up, left, down, or right depending
				# on which arrow key is pressed
				if event.key == pygame.K_UP:
					snake.move_up()
				elif event.key == pygame.K_LEFT:
					snake.move_left()
				elif event.key == pygame.K_DOWN:
					snake.move_down()
				elif event.key == pygame.K_RIGHT:
					snake.move_right()
				# pause the game is space is pressed
				elif event.key == pygame.K_SPACE:
					pause(score)
		if is_ate(snake, food):
			eat_sound()
			score += 1
			snake.length += 1
			# respawns the food to a new square
			food = Food()
		# slowly increments snake speed until it hits max
		snake_speed = snake.length / 2
		max_speed = 5
		if snake_speed > max_speed:
			snake_speed = 5

		updateGrid(score, snake, food)
		pygame.display.update()
		CLOCK.tick(15 + snake_speed)
	pygame.quit()

# Driver code
pygame.init()
play_game()

