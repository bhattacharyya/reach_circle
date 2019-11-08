#!/usr/bin/python
from tkinter import *
from tkinter.ttk import * 
import random
import time
import numpy as np

# Hyperparameters
alpha = 0.9
gamma = 1.0
epsilon = 0.0
episodes = 1000

mov_list = [-20,-10,10,20]
steps = 0

fout = open("logfile.txt","w")

#Set up Q table
state_space = {}
temp_list = []
for n in range(0,500,10):
	for m in range(0,360,10):
		temp_list.append((n,m))
for k in range(1800):
	state_space[k] = temp_list[k]

action_space = {}
temp_list = []
for n in mov_list:
	for m in mov_list:
		temp_list.append((m,n))
for k in range(16):
	action_space[k] = temp_list[k]

print(action_space)
q_table = np.zeros([len(state_space),len(action_space)])
#q_table = np.loadtxt("qtable.csv",delimiter=',')
print(q_table)

#Set up Environment and Simulation

def movement(): # Movement of Green Ball

	steps = 0
	checkpoint = 0
	pos_x1 = 50
	pos_y1 = 80 
	x1 = 10
	y1 = 10
	prev_move = (0,0)
	prev_dist_centre = 1000000

	game = 1
	reward = 0

	end = 1
	while end == 1:
		reward = 0
		state = list(state_space.keys())[list(state_space.values()).index((pos_x1, pos_y1))]
		steps += 1
		#reward = -1
		if game % episodes == 0:	
			end = 0
			np.savetxt("qtable.csv", q_table, delimiter=",")
			fout.write("qtable saved at " + str(steps) + " steps\n")

		if steps % 200 == 0:
			checkpoint = steps
			game += 1
			print("Game : "+str(self.game) + " lost")
			fout.write(str(steps) + " adjusting, time up\n")
			fout.write("game "+str(game) + " lost\n")
			fout.flush()
			new_x1 = (50 - pos_x1)
			new_y1 = (80 - pos_y1)
			#canvas.move(circle, new_x1, new_y1)
			pos_x1 += new_x1
			pos_y1 += new_y1		

		if steps % 1000 == 0:
			print("finished game : ",game)

		if game < 2000000:
			x1 = random.choice(mov_list)
			y1 = random.choice(mov_list)
			action = list(action_space.keys())[list(action_space.values()).index((x1, y1))]
			fout.write("Action randomly chosen : "+str(action)+"\n")
		else:
			if random.random() < epsilon:
				x1 = random.choice(mov_list)
				y1 = random.choice(mov_list)
				action = list(action_space.keys())[list(action_space.values()).index((x1, y1))]
			else:
				action = np.argmax(q_table[state])
				x1, y1 = action_space[action]
			#print("suggested",x1, y1)

		fout.write("Moving by "+str(x1)+", "+str(y1))

		if pos_x1 > 450:
			x1 = -10
		if pos_x1 < 25:
			x1 = 10
		if pos_y1 > 300:
			y1 = -10
		if pos_y1 < 25:
			y1 = 10  


		pos_x1 += x1
		pos_y1 += y1

		next_state = list(state_space.keys())[list(state_space.values()).index((pos_x1, pos_y1))]
		next_max = np.max(q_table[next_state])

		fout.write("Now at "+str(pos_x1)+", "+str(pos_y1)+"\n")

		if pos_x1 in [240,250,260] and pos_y1 in [170,180,190]:
			reward = 100
			game += 1
			print("Game : "+str(self.game) + " won")
			fout.write(str(steps) + " adjusting, target found "+str(pos_x1) +", " + str(pos_y1) + "\n")
			steps = checkpoint
			fout.write("Resetting to checkpoint steps "+str(checkpoint)+"\n")
			fout.write("game "+str(game) + " won\n")
			fout.flush()
			new_x1 = (50 - pos_x1)
			new_y1 = (80 - pos_y1)
			#canvas.move(circle, new_x1, new_y1)
			pos_x1 += new_x1
			pos_y1 += new_y1

		fout.write("Reward for the step : "+str(reward)+"\n")
		old_q_value = q_table[state, action]
		
		new_value = old_q_value + alpha * (reward + gamma * next_max)
		q_target = reward + gamma * next_max
		q_delta = q_target - old_q_value
		q_table[state, action] = old_q_value + alpha * q_delta


movement()