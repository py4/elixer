import sys
import pygame
from pygame import *
import random
from elixer import Elixer

click = False

class ElementController:
	def __init__(self, window):
		self.window = window
		self.zoom_rect = pygame.Rect(self.window.get_rect().right-50,50,15,200)
		self.zoom_scroll_rect = pygame.Rect(self.window.get_rect().right-50,50,15,30)
		self.zoom_rect_offset = 0
		self.initial_pos = 50
		self.event = None

	def render(self):
		# print("zoom rect offset: ",self.zoom_rect_offset)
		# print("previous pos: ",self.initial_pos)
		# print("mouse pos y:  ",pygame.mouse.get_pos()[1])
		pygame.draw.rect(self.window, (255,255,255), self.zoom_rect)
		self.render_zoom_rect()
		pygame.display.flip()		

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.initial_pos = pygame.mouse.get_pos()[1]

		if(self.zoom_scroll_rect.collidepoint(pygame.mouse.get_pos())):
			self.move_zoom_rect()
			return True	
		elif(self.zoom_rect.collidepoint(pygame.mouse.get_pos())):
			return True
		return False

	def render_zoom_rect(self):
		pygame.draw.rect(self.window, (40,40,40), self.zoom_scroll_rect)
		global click
		# if(click):
		# 	self.zoom_scroll_rect.top = pygame.mouse.get_pos()[1]
		# #self.zoom_scroll_rect.top += offset
		

	def move_zoom_rect(self):

		global click
		if(click):
			self.zoom_scroll_rect.top = pygame.mouse.get_pos()[1]-12
			self.render_zoom_rect()
			
		


class GUI:
	def __init__(self,height,width):
		pygame.init()
		self.core = Elixer()
		self.window = pygame.display.set_mode((height,width))
		self.element_controller = ElementController(self.window)
		self.camera_x_offset = 0
		self.camera_y_offset = 0
		self.render(0,0)
		self.initial_pos = pygame.mouse.get_pos()
		click = False
		self.run()

	def render(self,x_offset, y_offset):
		self.element_controller.render()
		self.core.push_siblings_with_collision(self.camera_x_offset, self.camera_y_offset, int(self.core.zoom_level))
		#self.core.push_children_with_collision(self.camera_x_offset, self.camera_y_offset, int(self.core.zoom_level-1))
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
					print("I'm scaling with this:  ", self.core.zoom_level)
					x1,y1 = Elixer.scale(self.core.zoom_level, array[i][0], array[i][1], max_x, min_x, max_y, min_y)
					x2,y2 = Elixer.scale(self.core.zoom_level, array[i+1][0], array[i+1][1], max_x, min_x, max_y, min_y)

					x1 += x_offset
					x2 += x_offset
					y1 += y_offset
					y2 += y_offset
					self.draw_line(x1, y1, x2, y2)
		self.update()

	def update(self):
		pygame.display.flip()

	def draw_line(self, x1,y1,x2,y2):
		pygame.draw.line(self.window, (255,255,255), (x1,y1), (x2,y2))
		#self.update()

	def run(self):
		global click
		time = pygame.time.get_ticks()
		time_step = 1
		clock = pygame.time.Clock()
		while True:
			event = pygame.event.wait()

			if event.type == pygame.QUIT:
				sys.exit(0)
			else:
				if event.type == pygame.MOUSEBUTTONDOWN:
					click = True
					self.initial_pos = pygame.mouse.get_pos()
				if event.type == pygame.MOUSEBUTTONUP:
					click = False

				if(click):

					if(self.element_controller.handle_event(event)):
						print(float((pygame.mouse.get_pos()[1] - 50)) / 50)

						
						self.core.zoom_level = float((pygame.mouse.get_pos()[1] - 50) / 50) + 1
						print("new zoom level:  ", self.core.zoom_level)
						print("---> Element Controller Event!")
					else:
						if not ((pygame.mouse.get_pos()[0] - self.initial_pos[0]) and pygame.mouse.get_pos()[1] - self.initial_pos[1]):
							continue
						self.camera_x_offset += pygame.mouse.get_pos()[0] - self.initial_pos[0]
						self.camera_y_offset += pygame.mouse.get_pos()[1] - self.initial_pos[1]
						self.initial_pos = pygame.mouse.get_pos()
						print("new x offset: ",self.camera_x_offset)
						print("new y offset: ",self.camera_y_offset)

					if(pygame.time.get_ticks() - time > time_step):
						self.window.fill((0,0,0))
						self.render(self.camera_x_offset, self.camera_y_offset)
						clock.tick(10)
						
						time = pygame.time.get_ticks()

click = False					
gui = GUI(640,480)