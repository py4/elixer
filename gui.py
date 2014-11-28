import sys
import pygame

class GUI:
	def __init__(self,height,width):
		pygame.init()
		self.window = pygame.display.set_mode((height,width))

	def update(self):
		pygame.display.flip()

	def draw_line(self, x1,y1,x2,y2):
		pygame.draw.line(self.window, (255,255,255), (x1,y1), (x2,y2))
		update()
