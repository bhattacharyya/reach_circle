#!/usr/bin/python
import random
import time
import numpy as np

# Set global values
alpha = 0.9
gamma = 1.0
epsilon = 0.0
episodes = 20000 # Number of games to be played
mov_list = [-40,-20,20,40] # Possible changes to x or y position
initial_pos_x1 = 40
initial_pos_y1 = 80
initial_pos_x2 = 160
initial_pos_y2 = 200

fout = open("logfile.txt","w")

#Set up Q table
state_space = {} # Set of all possible states
temp_list = []
state_temp_list = []

#State description for 1 ball
for n in range(0,500,20): 
	for m in range(0,360,20): 
		temp_list.append((n,m))

#State for the whole 2 ball system
for j in temp_list:
	for k in temp_list:
		state_temp_list.append((j,k))

for k in range(202500):
	state_space[k] = state_temp_list[k]

print(state_space[19])

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
	x1 = 20 # movement size in x direction
	y1 = 20 # movement size in y direction
	pos_x2 = initial_pos_x2 # x coordinate
	pos_y2 = initial_pos_y2 # y coordinate
	x2 = 20 # movement size in x direction
	y2 = 20 # movement size in y direction
	game = 0
	reward = 0
	win_counter = 0
	collision = 0
	green_collision_count = 0
	red_collision_count = 0
	tmp = 0

	end = 1
	while end == 1:
		reward = 0
		state = list(state_space.keys())[list(state_space.values()).index(((pos_x1, pos_y1),(pos_x2,pos_y2)))]
		steps += 1

		if game == episodes:
			end = 0
			print("Total games won : ",win_counter, "(",round(win_counter*100/episodes,2),"%)")
			print("collision_count : ",green_collision_count,red_collision_count)
			np.savetxt("qtable.csv", q_table, delimiter=",")
			fout.write("qtable saved at " + str(steps) + " steps\n")
			print("saved qtable after "+str(game)+" games")

		if game % 10000 == 0 and game != episodes and tmp == 0:
			np.savetxt("qtable.csv", q_table, delimiter=",")
			fout.write("qtable saved at " + str(steps) + " steps\n")
			print("saved qtable after "+str(game)+" games")
			tmp = 1

		if game % 10000 != 0:
			tmp = 0

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

			new_x2 = (initial_pos_x2 - pos_x2)
			new_y2 = (initial_pos_y2 - pos_y2)
			pos_x2 += new_x2
			pos_y2 += new_y2	

			collision = 0
			

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
		if pos_x1 > 459:
			x1 = -20
		if pos_x1 < 41:
			x1 = 20
		if pos_y1 > 319:
			y1 = -20
		if pos_y1 < 41:
			y1 = 20  

		# Update position
		pos_x1 += x1
		pos_y1 += y1

		# Check if green ball hit the red ball

		if (pos_x1 == pos_x2) and (pos_y1 == pos_y2):
			collision = 1
			reward = -200
			print("green collision", pos_x1, pos_y1, pos_x2, pos_y2)
			green_collision_count += 1		
			
		# Move the red ball
		if collision != 1:
			x2 = random.choice(mov_list)
			y2 = random.choice(mov_list)
			if pos_x2 > 459:
				x2 = -20
			if pos_x2 < 41:
				x2 = 20
			if pos_y2 > 319:
				y2 = -20
			if pos_y2 < 41:
				y2 = 20

			pos_x2 += x2
			pos_y2 += y2

			if (pos_x1 == pos_x2) and (pos_y1 == pos_y2):
				collision = 1
				print("red collision", pos_x1, pos_y1, pos_x2, pos_y2)
				red_collision_count += 1

		if collision == 1:
			game += 1	
			print("Game : "+str(game) + " lost due to collision")
			fout.write("game "+str(game) + " lost due to collision\n")
			fout.flush()
			steps = checkpoint # Reset number of steps to the start of the run
			
			# Reset to initial position
			new_x1 = (initial_pos_x1 - pos_x1)
			new_y1 = (initial_pos_y1 - pos_y1)
			pos_x1 += new_x1
			pos_y1 += new_y1

			new_x2 = (initial_pos_x2 - pos_x2)
			new_y2 = (initial_pos_y2 - pos_y2)
			pos_x2 += new_x2
			pos_y2 += new_y2

			collision = 0

		if pos_x1 == 240 and pos_y1 == 180:
			reward = 100
			game += 1
			print("Game : "+str(game) + " won")
			win_counter += 1
			steps = checkpoint # Reset number of steps to the start of the run
			fout.write("game "+str(game) + " won\n")
			fout.flush()

			# Reset to initial position
			new_x1 = (initial_pos_x1 - pos_x1)
			new_y1 = (initial_pos_y1 - pos_y1)
			pos_x1 += new_x1
			pos_y1 += new_y1

			new_x2 = (initial_pos_x2 - pos_x2)
			new_y2 = (initial_pos_y2 - pos_y2)
			pos_x2 += new_x2
			pos_y2 += new_y2
		
		# Update the Q table
		old_q_value = q_table[state, action]
		next_state = list(state_space.keys())[list(state_space.values()).index(((pos_x1, pos_y1),(pos_x2,pos_y2)))]
		next_max = np.max(q_table[next_state])
		q_target = reward + gamma * next_max
		q_delta = q_target - old_q_value
		q_table[state, action] = old_q_value + alpha * q_delta

movement()
