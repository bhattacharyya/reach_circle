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
initial_pos_x1 = 50
initial_pos_y1 = 80
mov_list = [-20,-10,10,20]

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
		self.x1 = 0
		self.y1 = 0

		self.game = 0
		self.reward = 0
		self.reset = 0
  
		# canvas object to create shape 
		self.canvas = Canvas(master,width=500, height=360, bg="black") 
		# creating circle 
		self.circle = self.canvas.create_oval(40, 70, 60, 90, fill = "green") 
		self.circle4 = self.canvas.create_oval(230, 160, 270, 200, outline = "yellow")
		
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
			self.reset = 0
			time.sleep(1)
		
		# Assess the state and find best action from Q table
		state = list(state_space.keys())[list(state_space.values()).index((self.pos_x1, self.pos_y1))]
		action = np.argmax(q_table[state])
		self.x1, self.y1 = action_space[action]
		
		# Bounce back from boundaries
		if self.pos_x1 > 479:
			self.x1 = -10
		if self.pos_x1 < 21:
			self.x1 = 10
		if self.pos_y1 > 339:
			self.y1 = -10
		if self.pos_y1 < 21:
			self.y1 = 10 

		# Update position
		self.canvas.move(self.circle, self.x1, self.y1)
		self.pos_x1 += self.x1
		self.pos_y1 += self.y1 

		self.steps += 1

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
		
		# If the ball finds the centre
		if self.pos_x1 == 250 and self.pos_y1 == 180:
			self.game += 1
			print("Game : "+str(self.game) + " won")
			self.steps = self.checkpoint # Reset number of steps to the start of the run
			self.reset = 1
		
		self.canvas.after(freq, self.movement)
	  
  
if __name__ == "__main__": 
  
	# object of class Tk, resposible for creating 
	# a tkinter toplevel window 
	master = Tk() 
	gfg = GFG(master)
	mainloop() 
