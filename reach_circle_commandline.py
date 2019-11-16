#!/usr/bin/python
import random
import time
import numpy as np

# Set global values
alpha = 0.9
gamma = 1.0
epsilon = 0.0
episodes = 200 # Number of games to be played
mov_list = [-20,-10,10,20] # Possible changes to x or y position

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
	pos_x1 = 50 # x coordinate
	pos_y1 = 80 # x coordinate
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
			new_x1 = (50 - pos_x1)
			new_y1 = (80 - pos_y1)
			pos_x1 += new_x1
			pos_y1 += new_y1		

		if game < 20000000: # arbitrarily chosen high value to prevent exploitation ; 
			#change above if exploitation is desired afterwards certain number of games
			x1 = random.choice(mov_list)
			y1 = random.choice(mov_list)
			action = list(action_space.keys())[list(action_space.values()).index((x1, y1))]
			fout.write("Action randomly chosen : "+str(action)+"\n")
		else:
			# Exploit based on epsilon probability
			if random.random() < epsilon:
				x1 = random.choice(mov_list)
				y1 = random.choice(mov_list)
				action = list(action_space.keys())[list(action_space.values()).index((x1, y1))]
			else:
				action = np.argmax(q_table[state])
				x1, y1 = action_space[action]


		fout.write("Moving by "+str(x1)+", "+str(y1))

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

		fout.write("Now at "+str(pos_x1)+", "+str(pos_y1)+"\n")

		if pos_x1 == 250 and pos_y1 == 180:
			reward = 100
			game += 1
			print("Game : "+str(game) + " won")
			win_counter += 1
			fout.write(str(steps) + " adjusting, target found "+str(pos_x1) +", " + str(pos_y1) + "\n")
			steps = checkpoint
			fout.write("Resetting to checkpoint steps "+str(checkpoint)+"\n")
			fout.write("game "+str(game) + " won\n")
			fout.flush()
			# Reset to initial position
			new_x1 = (50 - pos_x1)
			new_y1 = (80 - pos_y1)
			pos_x1 += new_x1
			pos_y1 += new_y1

		fout.write("Reward for the step : "+str(reward)+"\n")
		
		# Update the Q table
		old_q_value = q_table[state, action]
		next_state = list(state_space.keys())[list(state_space.values()).index((pos_x1, pos_y1))]
		next_max = np.max(q_table[next_state])
		q_target = reward + gamma * next_max
		q_delta = q_target - old_q_value
		q_table[state, action] = old_q_value + alpha * q_delta

movement()
