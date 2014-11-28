from data import DataHandler
from tree import QuadTree

class Elixer:
	def __init__(self):
		self.data_handler = DataHandler("data")
		self.tree = QuadTree(3)

	def get_current_coordinates(self):
		current_node = self.tree.current_value()
		return self.data_handler.load_data(current_node[0], current_node[1], current_node[2])