import numpy as np
import pygame
import random
pygame.init()

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
 
block_width = 100
display_width = 4 * block_width
display_height = 4 * block_width
game_display = pygame.display.set_mode((display_width, display_height))

FPS = 10
clock = pygame.time.Clock()

block_x, block_y = 0, 0
start_x, start_y = 0, 0
end_x, end_y	= display_width - block_width, display_height - block_width

hole_list = [[1, 1], [3, 1], [1, 2], [0, 3]]
score = 0
game_exit = False

# Q-table
Q = np.zeros([16, 4])

# hyper params
y = 0.9
num_episodes = 100
exploration = 1

pause = True
rewardList = []
for i in range(num_episodes):
	print "New Episode"
	# reset env
	s, new_s = 0, 0
	# print s
	# rTotal = 0
	exploration = 1. / (i + 1)
	

	block_x, block_y = 0, 0
	score = 0
	game_exit = False

	while not game_exit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_exit = True

		score = -1

		if block_x < 0:
			block_x = 0
			# game_exit = True

		elif block_x > display_width - block_width:
			block_x = display_width - block_width
			# game_exit = True

		elif block_y < 0:
			block_y = 0
			# game_exit = True

		elif block_y > display_height - block_width:
			block_y = display_height - block_width
			# game_exit = True

		if block_x == end_x and block_y == end_y:
			game_exit = True
			# score += 100

		for hole in hole_list:
			if block_x == hole[0] * block_width and block_y == hole[1] * block_width:
				game_exit = True
		
		
		
		# choose action
		tmp0 = random.randrange(0,4)
		tmp1 = random.randrange(0,4)
		tmp2 = random.randrange(0,4)
		tmp3 = random.randrange(0,4)
		tmp = np.array([tmp0,tmp1,tmp2,tmp3])
		# tmp = random.randrange(0,4)
		a = np.argmax(Q[s,:] + tmp * exploration * 80)
		# print tmp
		# take action
		if a == 0:
			block_y -= block_width
			if new_s > 3:
				new_s = s - 4
			else: score = -100
		elif a == 1:
			block_x += block_width
			if new_s % 4 != 3:
				new_s = s + 1
			else: score = -100
		elif a == 2:
			block_y += block_width
			if new_s < 12:
				new_s = s + 4
			else: score = -100
		elif a == 3:
			block_x -= block_width
			if new_s % 4 != 0:
				new_s = s - 1
			else: score = -100

		for hole in hole_list:
			if block_x == hole[0] * block_width and block_y == hole[1] * block_width:
				score = -100


		if block_x == end_x and block_y == end_y:
			game_exit = True
			score = 100

		# update Q-table
		print "UPDATING: " 
		Q[s, a] = score + (y * np.max(Q[new_s,:]))
		print Q
		print a
		print "---"
		print s,new_s
		print "---------------------------------------------------------------------------------"

		game_display.fill(black)
		pygame.draw.rect(game_display, red, [start_x, start_y, block_width, block_width])
		pygame.draw.rect(game_display, green, [end_x, end_y, block_width, block_width])
		
		for hole in hole_list:
			pygame.draw.rect(game_display, blue, [hole[0] * block_width, hole[1] * block_width, block_width, block_width])

		pygame.draw.rect(game_display, white, [block_x, block_y, block_width, block_width])
		pygame.display.flip()
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				pause = True

		# for debugging
		while pause:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					pause = False
		pause = False
		# pause = True

		s = new_s

print Q

pygame.quit()
quit()