from heapq import *

class Graph:

	def __init__(self):
		self.list = []
		self.nodes_count = 0
		self.edges_count = 0
		self.nodes_dict = {}
		self.reverse_nodes_dict = []

	def load_data(self, path):
		lines = []
		with open(path) as f:
			lines = f.readlines()
		self.nodes_count = int(lines[0])
		for i in range(1,self.nodes_count+1):
			splitted = lines[i].split(' ')
			x,y = float(splitted[0]), float(splitted[1])
			self.nodes_dict[(x,y)] = i-1
			self.reverse_nodes_dict.append((x,y))
			self.list.append([])

		for i in range(self.nodes_count+1,2*self.nodes_count + 1):
			current_node_id = i - (self.nodes_count+1)
			splitted = lines[i].split(' ')
			num_of_neighbors = int(splitted[0])
			self.edges_count += num_of_neighbors
			for j in range(0, num_of_neighbors):
				node_id, weight = int(splitted[2*j+1]), float(splitted[2*j+2])
				self.list[current_node_id].append((node_id, weight))
				# print("===============================")
				# print("node_id:  ", current_node_id)
				# print("x,y:  ", self.reverse_nodes_dict[current_node_id])
				# print("neighbor_id:  ", node_id)
				# print("x,y of neighbor:  ", self.reverse_nodes_dict[node_id])
				# print("weight:  ", weight)
				# print("===============================")

	def apply_dijkstra(self, source_node, dest_node):
		result = []
		dist = self.nodes_count * [None]
		parent = self.nodes_count * [None]
		queue = []
		for v in range(0, self.nodes_count):
			if(v == source_node):
				dist[v] = 0
			else:
				dist[v] = float("inf")
			parent[v] = None
			heappush(queue, (dist[v], v))
		while len(queue) > 0:
			dist_u,u = heappop(queue)
			if(u == dest_node):
				break
			for v,w in self.list[u]:
				alt = dist[u] + w
				if(alt < dist[v]):
					dist[v] = alt
					parent[v] = u
					heappush(queue, (dist[v], v))
		
		
		while(parent[dest_node] != None):
			result.append(dest_node)
			dest_node = parent[dest_node]
		result.append(source_node)
		return result[::-1]

g = Graph()
g.load_data("path/path.data")
print(g.apply_dijkstra(3,12))