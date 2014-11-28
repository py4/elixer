import sys
import pygame
import random
from elixer import Elixer

class GUI:
	def __init__(self,height,width):
		pygame.init()
		self.core = Elixer()
		self.window = pygame.display.set_mode((height,width))
		self.render(0,0)
		self.initial_pos = pygame.mouse.get_pos()
		self.camera_x_offset = 0
		self.camera_y_offset = 0
		self.click = False
		self.run()

	def render(self,x_offset, y_offset,scale_level=500):
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
					x1,y1 = self.scale(scale_level, array[i][0], array[i][1], max_x, min_x, max_y, min_y)
					x2,y2 = self.scale(scale_level, array[i+1][0], array[i+1][1], max_x, min_x, max_y, min_y)

					x1 += x_offset
					x2 += x_offset
					y1 += y_offset
					y2 += y_offset
					self.draw_line(x1, y1, x2, y2)
		


	def update(self):
		pygame.display.flip()

	def draw_line(self, x1,y1,x2,y2):
		pygame.draw.line(self.window, (255,255,255), (x1,y1), (x2,y2))
		self.update()

	def scale(self, level, x, y, max_x, min_x, max_y, min_y,):
		x = (x - min_x) / (max_x - min_x)
		y = (y - min_y) / (max_y - min_y)
		x *= level
		y *= level
		# x -= (max_x - min_x) / 2
		# y -= (max_y - min_y) / 2
		# scale = max(max_x - min_x, max_y - min_y)
		# x /= scale
		# y /= scale
		return x,y

	def run(self):
		time = pygame.time.get_ticks()
		time_step = 1
		clock = pygame.time.Clock()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				else:
					if event.type == pygame.MOUSEBUTTONDOWN:
						self.click = True
						self.initial_pos = pygame.mouse.get_pos()
					if event.type == pygame.MOUSEBUTTONUP:
						self.click = False

					if(self.click):
						self.camera_x_offset += pygame.mouse.get_pos()[0] - self.initial_pos[0]
						self.camera_y_offset += pygame.mouse.get_pos()[1] - self.initial_pos[1]
						self.initial_pos = pygame.mouse.get_pos()

						if(pygame.time.get_ticks() - time > time_step):
							self.window.fill((0,0,0))
							self.render(self.camera_x_offset, self.camera_y_offset)
							clock.tick(10)
							print("new x offset: ",self.camera_x_offset)
							print("new y offset: ",self.camera_y_offset)
							time = pygame.time.get_ticks()
					

gui = GUI(640,480)