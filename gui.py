import sys
import pygame
import random
from elixer import Elixer

class GUI:
	def __init__(self,height,width):
		pygame.init()
		self.core = Elixer()
		self.window = pygame.display.set_mode((height,width))
		self.render()
		self.run()

	def render(self):
		coordinates = self.core.get_current_coordinates()
		Xs = []
		Ys = []
		for h in coordinates:
			for t, array in h.items():
				for i in range(0,len(array)-1):
					Xs.append(array[i][0])
					Xs.append(array[i+1][0])
					Ys.append(array[i][1])
					Ys.append(array[i+1][1])

		max_x,min_x = max(Xs),min(Xs)
		max_y,min_y = max(Ys),min(Ys)

		for h in coordinates:
			for t, array in h.items():
				for i in range(0,len(array)-1):
					print("x1,y1 before:  ", array[i][0], array[i][1])
					#print("x2,y2 before:  ", array[i+1][0], array[i+1][1])
					x1,y1 = self.scale(array[i][0], array[i][1], max_x, min_x, max_y, min_y)
					x2,y2 = self.scale(array[i+1][0], array[i+1][1], max_x, min_x, max_y, min_y)
					print("x1,y1 after:  ", x1, y1)
					#print("x2,y2 after:  ", x2, y2)
					#print("x1,y1:  ",x1,y1)
					#print("x2,y2:  ",x2,y2)
					self.draw_line(x1, y1, x2, y2)
		#self.update()


	def update(self):
		pygame.display.flip()

	def draw_line(self, x1,y1,x2,y2):
		pygame.draw.line(self.window, (255,255,255), (x1,y1), (x2,y2))
		self.update()

	def scale(self, x, y, max_x, min_x, max_y, min_y):
		x = (x - min_x) / (max_x - min_x)
		y = (y - min_y) / (max_y - min_y)
		x *= 500
		y *= 500
		# x -= (max_x - min_x) / 2
		# y -= (max_y - min_y) / 2
		# scale = max(max_x - min_x, max_y - min_y)
		# x /= scale
		# y /= scale
		return x,y

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				else:
					None
					#self.render()
					#self.draw_line(random.randint(0,640),random.randint(0,480),random.randint(0,640),random.randint(0,480))
					#print ("pygame event ---> ",event)		

gui = GUI(640,480)