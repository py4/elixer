import sys
import pygame
from pygame import *
import random
from elixer import Elixer
from operator import itemgetter

click = False
search = False
source = None

def dist(pos1, pos2):
	return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

class ElementController:
	def __init__(self, window):
		self.window = window
		self.zoom_rect = pygame.Rect(self.window.get_rect().right-50,50,15,200)
		self.zoom_scroll_rect = pygame.Rect(self.window.get_rect().right-50,50,15,30)
		self.zoom_rect_offset = 0
		self.initial_pos = 50
		self.event = None

	def render(self):
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
		
	def move_zoom_rect(self):
		global click
		if(click):
			self.zoom_scroll_rect.top = pygame.mouse.get_pos()[1]-12
			self.render_zoom_rect()
			
class GUI:
	def __init__(self,height,width):
		pygame.init()
		self.core = Elixer()
		self.search_points = []
		self.window = pygame.display.set_mode((height,width))
		self.element_controller = ElementController(self.window)
		self.camera_x_offset = 0
		self.camera_y_offset = 0
		self.render(0,0)
		self.initial_pos = pygame.mouse.get_pos()
		self.last_click_pos = None
		click = False
		self.run()

	def render(self,x_offset, y_offset):
		self.element_controller.render()
		self.core.push_siblings_with_collision(self.camera_x_offset, self.camera_y_offset, int(self.core.zoom_level))
		
		coordinates = self.core.get_current_coordinates()
		
		if(len(coordinates) == 0):
			self.core.active_nodes = self.core.tree.get_nodes_at_height(self.core.zoom_level - 1)
			self.core.push_siblings_with_collision(self.camera_x_offset, self.camera_y_offset, int(self.core.zoom_level))
		
		if(len(coordinates) == 0):
			return

		# here was a code for selective scaling [ check out github ]		
		print("###########   I'm scaling with this:  ", self.core.zoom_level)
		print("###########   camera x offset:  ", self.camera_x_offset)
		print("###########   camera y offset:  ", self.camera_y_offset)

		self.draw_coordinates(coordinates)

	def draw_coordinates(self, coordinates):
		for h in coordinates:
			for t, array in h.items():
				for i in range(0,len(array)-1):
					
					x1, y1 = self.transform((array[i][0], array[i][1]))
					x2, y2 = self.transform((array[i+1][0], array[i+1][1]))

					self.draw_line(x1, y1, x2, y2)

		for i in range(0, len(self.search_points)-1):
			s = self.search_points[i]
			t = self.search_points[i+1]
			pygame.draw.line(self.window, (255,0,127), self.transform(s), self.transform(t))
		self.update()

	def transform(self, (x,y)):
		new_x,new_y = Elixer.scale(self.core.zoom_level, x, y, self.core.max_x, self.core.min_x, self.core.max_y, self.core.min_y)
		new_x += self.camera_x_offset
		new_y += self.camera_y_offset
		return new_x, new_y

	def reverse_transform(self, (x,y)):
		old_x, old_y = Elixer.reverse_scale(self.core.zoom_level, x, y, self.core.max_x, self.core.min_x, self.core.max_y, self.core.min_y)
		old_x -= self.camera_x_offset
		old_y -= self.camera_y_offset
		return old_x, old_y

	def update(self):
		pygame.display.flip()

	def draw_line(self, x1,y1,x2,y2):
		pygame.draw.line(self.window, (255,255,255), (x1,y1), (x2,y2))
		#self.update()


	def get_nearest_to(self, center):
		center = self.reverse_transform(center)
		best_pos = None
		min_dist = float("inf")
		for pos in list(self.core.graph.nodes_dict.keys()):
			if(dist(center, pos) < min_dist):
				min_dist = dist(center, pos)
				best_pos = pos
		return best_pos

	def get_knn(self, center, th = 10000):
		center = self.reverse_transform(center)
		res = []
		c = 0
		for pos in list(self.core.graph.nodes_dict.keys()):
			if(c == 200):
				break
			if(dist(center, pos) < th):#min_dist):
				res.append((dist(center, pos),pos))
				c += 1
		return sorted(res,key=itemgetter(0))

	def apply_search(self, source):
		print "&&&&&&&&&&&&&&&&&& SEARCHING &&&&&&&&&&&&&&&&"

		source = (source[0] - self.camera_x_offset, source[1] - self.camera_y_offset)
		dest = pygame.mouse.get_pos()
		dest = (dest[0] - self.camera_x_offset, dest[1] - self.camera_y_offset)

		source = self.get_knn(source)
		dest = self.get_knn(dest)

		if(len(source) == 0 or len(dest) == 0):
			print("NO NEIGHBOR FOUND")
			return
			#os.exit()

		done = False
		min_l = min(len(source), len(dest))
		for i in range(0, min_l):
			path = self.core.get_path_with_coordinations(source[i][1], dest[i][1])
			if(len(path) != 0):
				if(len(path) > 1 or path[0] == dest[i][1]):
					self.search_points = path
					break
			print("changing source and dest")
			i += min_l / 2

		# for dist1,s in source:
		# 	if(done):
		# 		break
		# 	c = 0
		# 	for dist2 ,d in dest:
		# 		path = self.core.get_path_with_coordinations(s, d)
		# 		if(path == []):
		# 			print(">>>> breaking because it had no out degree vertices")
		# 			break
		# 		if(c == 10):
		# 			print(">>>> breaking because we passed 10 points")
		# 			break
		# 		if(len(path) > 1):
		# 			done = True
		# 			print "--------------->   source:  ", self.transform(s)
		# 			print "--------------->   dest:  ", self.transform(d)
		# 			print "--------------->   distance:   ", dist2
		# 			self.search_points = path
		# 			break
		# 		c += 1

		self.window.fill((0,0,0))
		self.render(self.camera_x_offset, self.camera_y_offset)
		self.update()

	def run(self):
		global click, search, source
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
					self.last_click_pos = pygame.mouse.get_pos()

				if event.type == pygame.MOUSEBUTTONUP:
					click = False

					if(self.last_click_pos == pygame.mouse.get_pos() or dist(self.last_click_pos, pygame.mouse.get_pos()) < 10):
						if(search and source):
							print "######### [disable search] case1 #######"
							search = False
							self.apply_search(source)
						else:
							print "########## [enable search] ##########"
							search = True
							source = pygame.mouse.get_pos()
					else:
						print "######### [disable search] second case ############"
						search = False



				if(click):

					if(self.element_controller.handle_event(event)):

						a = float(self.element_controller.zoom_scroll_rect.top - 50) / 45 + 1

						if(int(self.core.zoom_level) != int(a)):
							print(">>>> ZOOM HAPPENED BROS! :)")
							print(">>>> from ", int(self.core.zoom_level), " to ", int(a))
							print(">>>> pushing children!")
							if(int(self.core.zoom_level) > int(a)):
								self.core.push_parents_with_collision(self.camera_x_offset, self.camera_y_offset, int(a))
							else:
								self.core.push_children_with_collision(self.camera_x_offset, self.camera_y_offset, int(a))
						
						self.core.zoom_level = a

					else:
						if not ((pygame.mouse.get_pos()[0] - self.initial_pos[0]) and pygame.mouse.get_pos()[1] - self.initial_pos[1]):
							continue

						self.camera_x_offset += pygame.mouse.get_pos()[0] - self.initial_pos[0]
						self.camera_y_offset += pygame.mouse.get_pos()[1] - self.initial_pos[1]

						self.initial_pos = pygame.mouse.get_pos()

					if(pygame.time.get_ticks() - time > time_step):
						self.window.fill((0,0,0))
						self.render(self.camera_x_offset, self.camera_y_offset)
						clock.tick(10)
						
						time = pygame.time.get_ticks()

click = False					
gui = GUI(640,480)