import os, json
from data import DataHandler


class QuadTree:
	def __init__(self, max_height):
		self.storage_size = (4**(max_height+1) - 1) / 3
		self.metadata = self.storage_size * [None]
		self.storage = []
		self.max_nodes = self.storage_size
		self.max_height = max_height
		self.root_node = 0
		self.current_node = 0
		self.load_storage()

	def load_storage(self):
		
		for h in range(0, self.max_height + 1):
				for y in range(0, 2 ** h):
					for z in range(0, 2 ** h):
						self.storage.append([h,y,z])
	
	def parent(self, node = None):
		if(node == None):
			node = self.current_node
		return node / 4

	def first_c(self, node = None):
		if(node == None):
			node = self.current_node
		return node * 4 + 1

	def second_c(self, node = None):
		if(node == None):
			node = self.current_node		
		return node * 4 + 2

	def third_c(self, node = None):
		if(node == None):
			node = self.current_node
		return node * 4 + 3

	def fourth_c(self, node = None):
		if(node == None):
			node = self.current_node
		return node * 4 + 4

	def current_value(self, node = None):
		if(node == None):
			node = self.current_node
		return self.storage[node]

	def value(self, id):
		return self.storage[id]

	def move_parent(self):
		self.current_node = parent()
	def move_first(self):
		self.current_node = first_c()
	def move_second(self):
		self.current_node = second_c()
	def move_third(self):
		self.current_node = third_c()
	def move_fourth(self):
		self.current_node = fourth_c()


	def get_children(self, node = None):
		if(node == None):
			node = self.current_node
		return [self.first_c(node), self.second_c(node), self.third_c(node), self.fourth_c(node)]