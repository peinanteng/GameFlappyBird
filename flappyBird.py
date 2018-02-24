import pygame, sys, random
from pygame.locals import *

pygame.init() # pygame initialisation

# <function>
def getMask(image):
	'''
	getMask() returns a matrix whose size is the same as the image
	each value in the matrix is either True or False, depending on whether the corresponding pixel is transparent
	returned matrix can be used to determine whether two sprites collide
	'''
	# initialise mask matrix
	mask = []
	# iterate each pixel using image width and height
	for x in range(image.get_width()):
		mask.append([])
		for y in range(image.get_height()):
			# convert into boolean value
			mask[x].append(bool(image.get_at((x, y))[3]))
	return mask

def checkCollide(birdMask, birdx, birdy, pipeMask, pipex, pipey):
	'''
	check whether bird collides with pipe using their masks and positions
	'''
	# get birdx and birdy, birdy needs to be converted into integer
	birdx = int(birdx)
	birdy = int(birdy)

	# initialise a matrix whose size is the same as the DISPLAYSURF with False values to indicate no sprites present
	raw = [[False] * HEIGHT for _ in range(WIDTH)]

	# use bird location and bird sprite size to update raw to indicate the presence of bird (False --> True)
	for i in range(birdx, birdx + birdWIDTH):
		for j in range(birdy, birdy + birdHEIGHT):
			if i >= 0 and i <= WIDTH and j >= 0 and j <= HEIGHT - baseHEIGHT:
				raw[i][j] = birdMask[i - birdx][j - birdy]

	# use pipe location and pipe size to determine whether pipe sprite and bird sprite are overlapped (collided)
	# if collided, return True, otherwise, return False
	for i in range(pipex, pipex + pipeWIDTH):
		for j in range(pipey, pipey + pipeHEIGHT):
			if i >= 0 and i < WIDTH and j >= 0 and j < HEIGHT - baseHEIGHT:
				if pipeMask[i - pipex][j - pipey] and raw[i][j]:
					return True
	return False

def starDisp(starCount):
	'''
	display current game difficulty on the top left corner of DISPLAYSURF
	more stars, more difficult
	'''

	# start location of star (top left)
	starx = 10
	stary = 10

	# update starx each time after adding one star
	for _ in range(starCount):
		DISPLAYSURF.blit(starImg, (starx, stary))
		starx += 24

def scoreDisp(score):
	'''
	display current score on the top left corner of DISPLAYSURF
	'''

	# convert score into string
	scoreStr = str(score)

	# start location of score (top left)
	digitx = 10
	digity = 40

	# update digitx each time after adding one digit
	for digit in scoreStr:
		DISPLAYSURF.blit(digitImgs[int(digit)], (digitx, digity))
		# different width of digit '1' and others
		if digit == '1':
			digitx += 25
		else:
			digitx += 28

def paraInit():
	'''
	parameter initialisation, used when game starts and restarts
	'''
	global birdy, velocity, wingOrder, bgOrder, pipeGapDecr, starCount, pipe1Gap, pipex1, pipey1, pipe2Gap, pipex2, pipey2, pipex1Passed, pipex2Passed, gameOver, score, collided, paused

	# birdy, velocity and wingOrder (determines which bird image to use)
	birdy = 40
	velocity = 0 # initialised to 0 and updated by gravity
	wingOrder = 0 # initialised to 0 and updated in while loop

	bgOrder = random.randint(0, 1)

	# determine game difficulty: easy, medium, hard, insane as well as different pipe gap decrement steps and star counts
	DIFFICULTY = random.choice(pipeGapDecrMap.keys())
	pipeGapDecr = pipeGapDecrMap[DIFFICULTY][0]
	starCount = pipeGapDecrMap[DIFFICULTY][1]

	# pipe gap and location
	# pipe initially horizontally located outside the canvas (pipex1, pipex2 > WIDTH)
	# pipe initial vertical location is randomly generated (range determined by pipe gap)
	# only upper pipe locations are given here since lower pipe locations can be calculated from upper pipe info
	# two pipes are used here to represent infinite number of pipes shown in the game
	# once one pipe disappears from the left of the canvas, it will reappear from the right

	pipe1Gap = pipeGAP
	pipex1 = 300
	pipey1 = random.randint(-(pipe1Gap / 2 + 180), -100)
	pipe2Gap = pipeGAP
	pipex2 = 470
	pipey2 = random.randint(-(pipe2Gap / 2 + 180), -100)

	# pipex1Passed and pipex2Passed indicate whether bird has passed each pipe
	pipex1Passed = 0
	pipex2Passed = 0

	score = 0 # current score

	# indicators
	gameOver = False # gameOver indicator
	collided = False # collide indicator
	paused = False # game pause indicator

# </function>

# <parameter>

FPS = 30 # frames per second
fpsClock = pygame.time.Clock() # game clock
WIDTH = 288 # canvas width
HEIGHT = 512 # canvas height
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32) # display surface
pygame.display.set_caption('Flappy Bird - nkukarl') # window caption

birdx = 40 # bird horizontal location
birdWIDTH = 34
birdHEIGHT = 24
GRAVITY = 0.25 # gravity, affecting birdy

pipeGAP = 140 # initial pipe gap

# pipeGapDecrMap: each entry --> difficulty: (pipeGapDecrStep, starCount)
pipeGapDecrMap = {'EASY': (0, 1), 'MEDIUM': (4, 2), 'HARD': (8, 3), 'INSANE': (16, 4)}
pipeWIDTH = 52
pipeHEIGHT = 320

# base sprite location and size
baseHEIGHT = 112
basex = 0
basey = HEIGHT - baseHEIGHT

# pauseIcon location and size
pauseWIDTH = 64
pauseHEIGHT = 64
pausex = (WIDTH - pauseWIDTH) / 2
pausey = (HEIGHT - pauseHEIGHT) / 2

# </parameter>

# <image>

# background and base
bgImgs = [pygame.image.load('sprites/bg_city.png').convert_alpha(), pygame.image.load('sprites/bg_scene.png').convert_alpha()]
baseImg = pygame.image.load('sprites/base.png').convert_alpha()

# bird: down, mid, up wing
birdImgs = [pygame.image.load('sprites/bird_down.png').convert_alpha(), pygame.image.load('sprites/bird_mid.png').convert_alpha(), pygame.image.load('sprites/bird_up.png').convert_alpha()]

# pipe: up and down
pipe_upImg = pygame.image.load('sprites/pipe_up.png').convert_alpha()
pipe_downImg = pygame.image.load('sprites/pipe_down.png').convert_alpha()

# star and score
starImg = pygame.image.load('sprites/star.png').convert_alpha()
digitImgs = [pygame.image.load('sprites/' + str(i) + '.png').convert_alpha() for i in range(10)]

# pause
pauseImg = pygame.image.load('sprites/pause.png').convert_alpha()

# message generation using http://fontmeme.com/pixel-fonts/
continueMsgImg = pygame.image.load('sprites/continueMsg.png').convert_alpha()
restartMsgImg = pygame.image.load('sprites/restartMsg.png').convert_alpha()
pauseMsgImg = pygame.image.load('sprites/pauseMsg.png').convert_alpha()
upMsgImg = pygame.image.load('sprites/upMsg.png').convert_alpha()
overMsgImg = pygame.image.load('sprites/overMsg.png').convert_alpha()

# masks: birdMask has to be defined inside the while loop since birdImg changes over time
pipe_upMask = getMask(pipe_upImg)
pipe_downMask = getMask(pipe_downImg)

# </image>

# <audio>

# sound effect files from http://themushroomkingdom.net/media/smb/wav
collideSound = pygame.mixer.Sound('audio/collide.wav')
flySound = pygame.mixer.Sound('audio/fly.wav')
pointSound = pygame.mixer.Sound('audio/point.wav')
pauseSound = pygame.mixer.Sound('audio/pause.wav')

# </audio>

# <initialisation>

# initialise parameters to start game
paraInit()
# </initialisation>

while True:

	# add background
	DISPLAYSURF.blit(bgImgs[bgOrder], (0, 0))

	# get birdImg and birdMask
	birdImg = birdImgs[wingOrder]
	birdMask = getMask(birdImg)

	# add bird
	DISPLAYSURF.blit(birdImg, (birdx, birdy))

	# add pipes: pipe1 and pipe2, up and down
	# location of lower pipe is calculated using upper pipe vertical location plus pipe height and gap size
	
	DISPLAYSURF.blit(pipe_upImg, (pipex1, pipey1))
	DISPLAYSURF.blit(pipe_downImg, (pipex1, pipey1 + pipeHEIGHT + pipe1Gap))

	DISPLAYSURF.blit(pipe_upImg, (pipex2, pipey2))
	DISPLAYSURF.blit(pipe_downImg, (pipex2, pipey2 + pipeHEIGHT + pipe2Gap))

	# add base
	DISPLAYSURF.blit(baseImg, (basex, basey))
	
	# add star to indicate difficulty
	starDisp(starCount)
	
	# check if collided
	# bird might collide with pipe1 (up and down), pipe2 (up and down), sky and ground
	collided = checkCollide(birdMask, birdx, birdy, pipe_upMask, pipex1, pipey1) or checkCollide(birdMask, birdx, birdy, pipe_downMask, pipex1, pipey1 + pipeHEIGHT + pipe1Gap) or checkCollide(birdMask, birdx, birdy, pipe_upMask, pipex2, pipey2) or checkCollide(birdMask, birdx, birdy, pipe_downMask, pipex2, pipey2 + pipeHEIGHT + pipe2Gap) or birdy <= 0 or birdy >= HEIGHT - baseHEIGHT - birdHEIGHT

	if collided:

		# add restart message and game over message

		DISPLAYSURF.blit(restartMsgImg, (0, 440))
		DISPLAYSURF.blit(overMsgImg, (18, 200))

		# update game over state and play collideSound
		if gameOver == False:
			collideSound.play()
			gameOver = True

		# wait to exit game or to restart
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				# up arrow key to restart
				if event.key == K_UP:
					# parameter initialisation
					paraInit()
					
	else: # not collided
		
		if not paused: # in game
			
			# add play message and pause message
			DISPLAYSURF.blit(upMsgImg, (0, 440))
			DISPLAYSURF.blit(pauseMsgImg, (0, 465))
			
			# update wing order in each frame to show wing motion
			wingOrder = (wingOrder + 1) % 3

			# update bird velocity and location
			velocity += GRAVITY
			birdy += velocity

			# pipe location looping
			if pipex1 - 2 < -pipeWIDTH: # pipe1 disappears
				pipex1 = WIDTH # pipe1 reappears
				pipey1 = random.randint(-(pipe1Gap / 2 + 180), -100) # random vertical location
				pipe1Gap -= pipeGapDecr # reduce gap size based on difficulty
				pipex1Passed = 0 # reset pass indicator
			else:
				pipex1 = pipex1 - 2 # move pipe1 by 2 pixels to the left
				if pipex1 + pipeWIDTH < birdx: # bird passes pipe
					pipex1Passed += 1 # increase pass indicator by 1
				if pipex1Passed == 1: # only update score when indicator is 1
					score += 15 - int(pipe1Gap / 10) # gap size based score
					pointSound.play() # play point winning sound

			# pipe2 same as pipe1
			if pipex2 - 2 < -pipeWIDTH:
				pipex2 = WIDTH
				pipey2 = random.randint(-(pipe2Gap / 2 + 180), -100)
				pipe2Gap -= pipeGapDecr
				pipex2Passed = 0
			else:
				pipex2 = pipex2 - 2
				if pipex2 + pipeWIDTH < birdx:
					pipex2Passed += 1
				if pipex2Passed == 1:
					score += 15 - int(pipe2Gap / 10)
					pointSound.play()

			# base location looping
			basex -= 2 # move base by 2 pixels to the left
			if basex < -20: # base reappears from the right of canvas to create base moving effect
				basex = 0

			# wait to exit game, key up to move bird or esc to pause
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == KEYDOWN:
					if event.key == K_UP: # move bird
						velocity = -3 # update bird velocity to upper direction
						flySound.play() # play fly sound
					if event.key == K_ESCAPE:
						paused = True # update pause indicator
						pauseSound.play() # play pause sound

		else:
			# add pause icon and continue message
			DISPLAYSURF.blit(pauseImg, (pausex, pausey))
			DISPLAYSURF.blit(continueMsgImg, (0, 440))

			# wait to exit game or key up to continue
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == KEYDOWN and event.key == K_UP:
					paused = False # update pause indicator
					

	scoreDisp(score) # display score

	pygame.display.update() # update canvas
	fpsClock.tick(FPS) # clock tick