#!/usr/bin/python
'''
This code is same as reach_circle_commandline.py with only
one exception. There are multiple possible initial position
rather than just 1 of them.
'''

import random
import time
import numpy as np

# Set global values
alpha = 0.9
gamma = 1.0
epsilon = 0.0
episodes = 80000 # Number of games to be played
mov_list = [-20,-10,10,20] # Possible changes to x or y position
initial_pos_x1 = 50
initial_pos_y1 = 80

fout = open("logfile.txt","w")

#Set up Q table
state_space = {} # Set of all possible states
temp_list = []
for n in range(0,500,10): 
	for m in range(0,360,10): 
		temp_list.append((n,m))
for k in range(1800):
	state_space[k] = temp_list[k]

action_space = {} # Set of all possible actions
temp_list = []
for n in mov_list:
	for m in mov_list:
		temp_list.append((m,n))
for k in range(16):
	action_space[k] = temp_list[k]

q_table = np.zeros([len(state_space),len(action_space)]) # Use this for generating new Q table
#q_table = np.loadtxt("qtable.csv",delimiter=',') # Uncomment this to read from an existing q table

def movement(): # Movement of Green Ball

	# Set local variables
	steps = 0
	checkpoint = 0
	pos_x1 = initial_pos_x1 # x coordinate
	pos_y1 = initial_pos_y1 # y coordinate
	x1 = 10 # movement size in x direction
	y1 = 10 # movement size in y direction
	game = 1
	reward = 0
	win_counter = 0

	end = 1
	while end == 1:
		reward = 0
		state = list(state_space.keys())[list(state_space.values()).index((pos_x1, pos_y1))]
		steps += 1

		if game == episodes:	
			end = 0
			print("Total games won : ",win_counter, "(",round(win_counter*100/episodes,2),"%)")
			np.savetxt("qtable.csv", q_table, delimiter=",")
			fout.write("qtable saved at " + str(steps) + " steps\n")
			print("saved qtable")

		# If max steps is reached
		if steps % 200 == 0:
			checkpoint = steps
			game += 1
			print("Game : "+str(game) + " lost")
			fout.write(str(steps) + " adjusting, time up\n")
			fout.write("game "+str(game) + " lost\n")
			fout.flush()

			# Reset to initial position
			new_x1 = (initial_pos_x1 - pos_x1)
			new_y1 = (initial_pos_y1 - pos_y1)
			pos_x1 += new_x1
			pos_y1 += new_y1		

		if game < 20000000: # arbitrarily chosen high value to prevent exploitation ; 
			#change above if exploitation is desired afterwards certain number of games
			x1 = random.choice(mov_list)
			y1 = random.choice(mov_list)
			action = list(action_space.keys())[list(action_space.values()).index((x1, y1))]
		else:
			# Exploit based on epsilon probability
			if random.random() < epsilon:
				x1 = random.choice(mov_list)
				y1 = random.choice(mov_list)
				action = list(action_space.keys())[list(action_space.values()).index((x1, y1))]
			else:
				action = np.argmax(q_table[state])
				x1, y1 = action_space[action]

		# Bounce back from boundaries
		if pos_x1 > 479:
			x1 = -10
		if pos_x1 < 21:
			x1 = 10
		if pos_y1 > 339:
			y1 = -10
		if pos_y1 < 21:
			y1 = 10  

		# Update position
		pos_x1 += x1
		pos_y1 += y1

		if pos_x1 == 250 and pos_y1 == 180:
			reward = 100
			game += 1
			print("Game : "+str(game) + " won")
			win_counter += 1
			steps = checkpoint # Reset number of steps to the start of the run
			fout.write("game "+str(game) + " won\n")
			fout.flush()
			# Reset to initial position
			rand_pos_x1 = random.choice([50,100,150,200,300,350,400])
			rand_pos_y1 = random.choice([80,120,240,280]) 
			new_x1 = (rand_pos_x1 - pos_x1)
			new_y1 = (rand_pos_y1 - pos_y1)
			pos_x1 += new_x1
			pos_y1 += new_y1
		
		# Update the Q table
		old_q_value = q_table[state, action]
		next_state = list(state_space.keys())[list(state_space.values()).index((pos_x1, pos_y1))]
		next_max = np.max(q_table[next_state])
		q_target = reward + gamma * next_max
		q_delta = q_target - old_q_value
		q_table[state, action] = old_q_value + alpha * q_delta

movement()
