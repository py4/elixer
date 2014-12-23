from data import DataHandler
from tree import QuadTree
import os, json
import codecs
from graph import *
import multiprocessing
import threading

class Elixer:
	def __init__(self):
		self.min_x = 100000000000
		self.min_y = 100000000000
		self.max_x = 0
		self.max_y = 0
		self.height = 480
		self.width = 640

		self.graph = Graph()
		self.graph.load_data("path/path.data")

		# thread = threading.Thread(target=self.graph.load_data, args=["path/path.data"])
		# thread.start()

    #threads.append(thread)
		# process = multiprocessing.Process(target = self.graph.load_data, args=["path/path.data"])
		# process.start()

		self.data_handler = DataHandler("data")
		self.tree = QuadTree(3)
		self.active_nodes = []
		self.zoom_level = 1
		self.fill_metadata()
		self.active_nodes.append(0)

	def get_path_with_coordinations(self, source, destination):
		result = []
		for node in self.get_path(source, destination):
			result.append(self.graph.reverse_nodes_dict[node])
		return result

	def get_path(self, source, destination):
		if(source.__class__.__name__ == 'tuple'):
			#path, cost = self.graph.apply_dijkstra(self.graph.nodes_dict[source], self.graph.nodes_dict[destination])
			path = self.graph.apply_a_star(self.graph.nodes_dict[source], self.graph.nodes_dict[destination])
			return path
		else:
			#path, cost = self.graph.apply_dijkstra(source, destination)
			path = self.graph.apply_a_star(source, destination)
			return path

	def fill_metadata(self):
		i = 0
		for h in range(0, self.tree.max_height + 1):
			for y in range(0, 2 ** h):
					for z in range(0, 2 ** h):
						self.tree.metadata[i] = {}
						path = DataHandler.get_path(h,y,z)
						self.tree.metadata[i] = {}

						if os.path.isfile(path):
							
							data = json.load(codecs.open(path, 'r', 'latin-1'))
							
							self.tree.metadata[i]["bbox"] = {}
							self.tree.metadata[i]["bbox"]["min_x"] = data["bbox"][0]
							self.tree.metadata[i]["bbox"]["min_y"] = data["bbox"][1]
							self.tree.metadata[i]["bbox"]["max_x"] = data["bbox"][2]
							self.tree.metadata[i]["bbox"]["max_y"] = data["bbox"][3]
								
							self.min_x = min([self.min_x, data["bbox"][0]])
							self.min_y = min([self.min_y, data["bbox"][1]])
							self.max_x = max([self.max_x, data["bbox"][2]])
							self.max_y = max([self.max_y, data["bbox"][3]])

						i += 1
	@classmethod
	def scale(self, level, x, y, max_x, min_x, max_y, min_y):
		
		new_x = (((x - min_x) / (max_x - min_x)) * (640 * level))
		new_y = (((y - min_y) / (max_y - min_y)) * (480 * level))
		return new_x, new_y

	@classmethod
	def reverse_scale(self, level, new_x, new_y, max_x, min_x, max_y, min_y):
		old_x = (float(new_x) / (640 * level)) * (max_x - min_x) + min_x
		old_y = (float(new_y) / (480 * level)) * (max_y - min_y) + min_y
		return old_x, old_y
		
	def get_current_coordinates(self):
		coordinates = []
		for node in self.active_nodes:
			value = self.tree.value(node)
			coordinates += self.data_handler.load_data(value[0], value[1], value[2])
		return coordinates

	def push_siblings_with_collision(self, camera_x_offset, camera_y_offset, zoom_level = None):
		if(zoom_level == None):
			zoom_level = self.zoom_level
		if(self.active_nodes == [0]):
			return

		parents = set()
		for node in self.active_nodes:
			parents.add(self.tree.parent(node))
		self.active_nodes = []
		for parent in parents:
			self.active_nodes += self.get_children_with_collision(parent, camera_x_offset, camera_y_offset, zoom_level+1)
		print(">>> just pushed these nodes with collision: ", self.active_nodes)

	def push_parents_with_collision(self, camera_x_offset, camera_y_offset, zoom_level = None):
		if(zoom_level == None):
			zoom_level = self.zoom_level
		if(self.active_nodes == [0]):
			return

		self.active_nodes = []
		for node in self.active_nodes:
			if(has_collision(node, camera_x_offset, camera_y_offset, zoom_level + 1)):
				self.active_nodes.push(node)

	def push_children_with_collision(self, camera_x_offset, camera_y_offset, zoom_level = None):
		if(zoom_level == None):
			zoom_level = self.zoom_level
		result = []
		for node in self.active_nodes:
			result += self.get_children_with_collision(node, camera_x_offset, camera_y_offset, zoom_level + 1)
		print("children:   ", result)
		self.active_nodes = result

	def has_collision(self, node, camera_x_offset, camera_y_offset, scale_level):
		min_x = self.tree.metadata[node]["bbox"]["min_x"]
		min_y = self.tree.metadata[node]["bbox"]["min_y"]
		max_x = self.tree.metadata[node]["bbox"]["max_x"]
		max_y = self.tree.metadata[node]["bbox"]["max_y"]

		min_x, min_y = self.scale(scale_level, min_x, min_y, self.max_x, self.min_x, self.max_y, self.min_y)
		max_x, max_y = self.scale(scale_level, max_x, max_y, self.max_x, self.min_x, self.max_y, self.min_y)

		min_x += camera_x_offset
		max_x += camera_x_offset
		min_y += camera_y_offset
		max_y += camera_y_offset

		if(min_x < 640 and max_x > 0 and min_y < 480 and max_y > 0):
			return True
		return False


	def get_children_with_collision(self, current_node, camera_x_offset, camera_y_offset, scale_level = None):
		if(scale_level == None):
			scale_level = self.zoom_level + 1

		nodes = []
		for node in self.tree.get_children(current_node):

			if(node >= self.tree.storage_size):
				continue
			if(self.tree.metadata[node] == {}):
				continue
			
			if(self.has_collision(node, camera_x_offset, camera_y_offset, scale_level)):
				nodes.append(node)
			print("collision nodes:  ", nodes)
			
		return nodes