#!/usr/bin/python
from tkinter import *
from tkinter.ttk import * 
import random
import time
import numpy as np

# Set global values
alpha = 0.9
gamma = 1.0
freq = 100 # Frequency of refreshing the canvas

#Initialize position for the ball
initial_pos_x1 = 40
initial_pos_y1 = 80
initial_pos_x2 = 160
initial_pos_y2 = 200
mov_list = [-40,-20,20,40]

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

q_table = np.loadtxt("qtable.csv",delimiter=',')

#Set up Environment and Simulation
class GFG: 
	
	def __init__(self, master = None): 
		# Set up local variables
		self.steps = 0
		self.checkpoint = 0
		self.master = master 
		self.pos_x1 = initial_pos_x1
		self.pos_y1 = initial_pos_y1
		self.x1 = 20
		self.y1 = 20
		self.pos_x2 = initial_pos_x2
		self.pos_y2 = initial_pos_y2
		self.x2 = 20
		self.y2 = 20

		self.game = 0
		self.reward = 0
		self.reset = 0
		self.collision = 0
		self.green_collision = 0
		self.red_collision = 0
  
		# canvas object to create shape 
		self.canvas = Canvas(master,width=500, height=360, bg="black") 
		# creating circle 
		self.circle = self.canvas.create_oval(30, 70, 50, 90, fill = "green")
		self.circle3 = self.canvas.create_oval(150, 190, 170, 210, fill = "red") 
		self.circle4 = self.canvas.create_oval(220, 160, 260, 200, outline = "yellow")

		self.canvas.pack() 
		
		self.movement() 

	def movement(self): # Movement of Green Ball

		if self.reset == 1:
			# Reset ball to initial position and update coordinates
			new_x1 = (initial_pos_x1 - self.pos_x1)
			new_y1 = (initial_pos_y1 - self.pos_y1)
			self.canvas.move(self.circle,new_x1,new_y1)
			self.pos_x1 += new_x1
			self.pos_y1 += new_y1

			new_x2 = (initial_pos_x2 - self.pos_x2)
			new_y2 = (initial_pos_y2 - self.pos_y2)
			self.canvas.move(self.circle3,new_x2,new_y2)
			self.pos_x2 += new_x2
			self.pos_y2 += new_y2

			self.reset = 0
			time.sleep(1)
		
		# Assess the state and find best action from Q table
		state = list(state_space.keys())[list(state_space.values()).index(((self.pos_x1, self.pos_y1),(self.pos_x2,self.pos_y2)))]
		action = np.argmax(q_table[state])
		self.x1, self.y1 = action_space[action]

		#Use below only to test the non-learned behavior
		#self.x1 = random.choice(mov_list)
		#self.y2 = random.choice(mov_list)
		
		# Bounce back from boundaries
		if self.pos_x1 > 459:
			self.x1 = -20
		if self.pos_x1 < 41:
			self.x1 = 20
		if self.pos_y1 > 319:
			self.y1 = -20
		if self.pos_y1 < 41:
			self.y1 = 20 

		# Update position
		self.canvas.move(self.circle, self.x1, self.y1)
		self.pos_x1 += self.x1
		self.pos_y1 += self.y1 

		self.steps += 1

		# Did collision happen ?
		if self.pos_x1 == self.pos_x2 and self.pos_y1 == self.pos_y2:
			self.collision = 1
			self.green_collision += 1
			print("collision after green ball update")

		# Move the red ball (only if green hasn't collided to it)
		if self.collision != 1:
			self.x2 = random.choice(mov_list)
			self.y2 = random.choice(mov_list)
			if self.pos_x2 > 459:
				self.x2 = -20
			if self.pos_x2 < 41:
				self.x2 = 20
			if self.pos_y2 > 319:
				self.y2 = -20
			if self.pos_y2 < 41:
				self.y2 = 20

			# Update position
			self.canvas.move(self.circle3, self.x2, self.y2)
			self.pos_x2 += self.x2
			self.pos_y2 += self.y2

			# Did collision happen ?
			if self.pos_x1 == self.pos_x2 and self.pos_y1 == self.pos_y2:
				self.collision = 1
				self.red_collision += 1
				print("collision after red ball update")

		# If 200 steps are over
		if self.steps % 200 == 0:
			self.checkpoint = self.steps
			self.game += 1
			print("Game : "+str(self.game) + " lost")
			new_x1 = (initial_pos_x1 - self.pos_x1)
			new_y1 = (initial_pos_y1 - self.pos_y1)
			self.canvas.move(self.circle, new_x1, new_y1)
			self.pos_x1 += new_x1
			self.pos_y1 += new_y1

			new_x2 = (initial_pos_x2 - self.pos_x2)
			new_y2 = (initial_pos_y2 - self.pos_y2)
			self.canvas.move(self.circle3, new_x2, new_y2)
			self.pos_x2 += new_x2
			self.pos_y2 += new_y2
			self.collision = 0		
		
		# If the ball finds the centre
		if (self.pos_x1 == 240 and self.pos_y1 == 180):
			self.game += 1
			print("Game : "+str(self.game) + " won")
			self.steps = self.checkpoint # Reset number of steps to the start of the run
			self.reset = 1

		# If the balls collide
		if self.collision == 1:
			self.game += 1
			print("Game : "+str(self.game) + " lost")
			print("green_collisions : ",self.green_collision,"red_collisions : ",self.red_collision)
			self.steps = self.checkpoint # Reset number of steps to the start of the run
			self.reset = 1
			self.collision = 0
		
		self.canvas.after(freq, self.movement)
	  
  
if __name__ == "__main__": 
  
	# object of class Tk, resposible for creating 
	# a tkinter toplevel window 
	master = Tk() 
	gfg = GFG(master)
	mainloop() 
