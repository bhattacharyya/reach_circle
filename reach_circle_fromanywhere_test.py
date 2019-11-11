#!/usr/bin/python
from tkinter import *
from tkinter.ttk import * 
import random
import time
import numpy as np

# Hyperparameters
alpha = 0.9
gamma = 1.0
freq = 100

initial_pos_x1 = 50
initial_pos_y1 = 80

mov_list = [-20,-10,10,20]
steps = 0

fout = open("logfile2.txt","w")

#Set up Q table
state_space = {}
temp_list = []
for n in range(0,500,10):
	for m in range(0,360,10):
		temp_list.append((n,m))
for k in range(1800):
	state_space[k] = temp_list[k]
#print(state_space)
action_space = {}
temp_list = []
for n in mov_list:
	for m in mov_list:
		temp_list.append((m,n))
for k in range(16):
	action_space[k] = temp_list[k]

q_table = np.loadtxt("qtable.csv",delimiter=',')
print(q_table)

#Set up Environment and Simulation
class GFG: 
	
	def __init__(self, master = None): 
		self.steps = 0
		self.checkpoint = 0
		self.master = master 
		self.pos_x1 = initial_pos_x1
		self.pos_y1 = initial_pos_y1
		self.x1 = 0
		self.y1 = 0

		self.game = 1
		self.reward = 0
		self.reset = 0
  
		# canvas object to create shape 
		self.canvas = Canvas(master,width=500, height=360, bg="black") 
		# creating circle 
		self.circle = self.canvas.create_oval( 
						 40, 70, 60, 90, fill = "green") 
		self.circle4 = self.canvas.create_oval( 
						 230, 160, 270, 200, outline = "yellow")
		self.canvas.pack() 
		
		self.movement() 

	def movement(self): # Movement of Green Ball

		if self.reset == 1:
			rand_pos_x1 = random.choice([50,100,150,200,300,350,400])
			rand_pos_y1 = random.choice([80,120,240,280]) 
			new_x1 = (rand_pos_x1 - self.pos_x1)
			new_y1 = (rand_pos_y1 - self.pos_y1)
			self.canvas.move(self.circle,new_x1,new_y1)
			self.pos_x1 += new_x1
			self.pos_y1 += new_y1
			print("After resetting state is", self.pos_x1, self.pos_y1)
			self.reset = 0
			time.sleep(1)
		
		state = list(state_space.keys())[list(state_space.values()).index((self.pos_x1, self.pos_y1))]
		print("state is : ",self.pos_x1, self.pos_y1)
		action = np.argmax(q_table[state])
		self.x1, self.y1 = action_space[action]
				
		if self.pos_x1 > 450:
			self.x1 = -10
		if self.pos_x1 < 25:
			self.x1 = 10
		if self.pos_y1 > 300:
			self.y1 = -10
		if self.pos_y1 < 25:
			self.y1 = 10 


		self.canvas.move(self.circle, self.x1, self.y1)
		self.pos_x1 += self.x1
		self.pos_y1 += self.y1 
		print("After moving",self.x1, self.y1, "state is", self.pos_x1, self.pos_y1)

		self.steps += 1
		if self.steps % 200 == 0:
			self.checkpoint = self.steps
			self.game += 1
			print("Game : "+str(self.game) + " lost")
			fout.write(str(self.steps) + " adjusting, time up\n")
			fout.write("game "+str(self.game) + " lost\n")
			fout.flush()
			rand_pos_x1 = random.choice([50,100,150,200,300,350,400])
			rand_pos_y1 = random.choice([80,120,240,280]) 
			new_x1 = (rand_pos_x1 - self.pos_x1)
			new_y1 = (rand_pos_y1 - self.pos_y1)
			self.canvas.move(self.circle, new_x1, new_y1)
			self.pos_x1 += new_x1
			self.pos_y1 += new_y1
			print("200th step",self.pos_x1, self.pos_y1)
		
		
		if self.pos_x1 == 250 and self.pos_y1 == 180:
			self.game += 1
			print("Game : "+str(self.game) + " won")
			fout.write(str(self.steps) + " adjusting, target found\n")
			fout.write("game "+str(self.game) + " won\n")
			fout.flush()
			self.steps = self.checkpoint
			self.reset = 1
		
		self.canvas.after(freq, self.movement)
	  
  
if __name__ == "__main__": 
  
	# object of class Tk, resposible for creating 
	# a tkinter toplevel window 
	master = Tk() 
	gfg = GFG(master)
	mainloop() 
