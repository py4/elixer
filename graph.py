from heapq import *
import sys
import time

class Graph:

	def __init__(self):
		self.list = []
		self.nodes_count = 0
		self.edges_count = 0
		self.nodes_dict = {}
		self.reverse_nodes_dict = []
		self.cache = {}
		self.cache_dist = {}

	def clear_cache(self):
		self.cache = {}

	def is_cache_enable(self):
		if(len(list(self.cache.keys()))):
			return True
		return False

	def get_cache_rep(self):
		if(self.is_cache_enable()):
			return list(self.cache.keys())[0]
		else:
			return None

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

	def apply_dijkstra(self, source_node, dest_node):
		if(len(self.list[source_node]) == 0):
			self.cache = {}
			self.cache_dist = {}
			print(" --- !!!! --- this node does not have any out degre")
			return []

		rep = self.get_cache_rep()
	
		if(rep == source_node):
			print "reading from cache!"
			result = self.get_path(self.cache[rep], source_node, dest_node), self.cache_dist[rep]
			return result

		result = []
		dist = self.nodes_count * [None]
		parent = self.nodes_count * [None]
		cost = self.nodes_count * [None]
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
			for v,w in self.list[u]:
				alt = dist[u] + w
				if(alt < dist[v]):
					dist[v] = alt
					parent[v] = u
					heappush(queue, (dist[v], v))


		self.cache = {}		
		self.cache_dist = {}
		self.cache[source_node] = parent
		self.cache_dist[source_node] = dist[dest_node]
		return self.get_path(parent, source_node, dest_node), dist[dest_node]

	def cost_estimate(self, source_node, dest_node):
		source_node = self.reverse_nodes_dict[source_node]
		dest_node = self.reverse_nodes_dict[dest_node]
		return 100*(abs(source_node[0] - dest_node[0]) + abs(source_node[1] - dest_node[1]))

	def apply_a_star(self, source_node, dest_node):
		print(">>> apply A* <<<")
		closed_set = self.nodes_count * [None]
		openset = []
		open_set_keys = self.nodes_count * [None]
		result = []
		parent = []
		g_score = self.nodes_count * [float("inf")]
		f_score = self.nodes_count * [float("inf")]
		parent = self.nodes_count * [None]
		cost = self.nodes_count * [None]

			
		g_score[source_node] = 0
		f_score[source_node] = g_score[source_node] + self.cost_estimate(source_node, dest_node)
		heappush(openset, (f_score[source_node], source_node))

		while len(openset):
			dist_current, current = heappop(openset)
			if(current == dest_node):
				print "found it!"
				return self.get_path(parent, source_node, dest_node)

			closed_set[current] = True

			for neighbor,dist in self.list[current]:
				if(closed_set[neighbor]):
					continue
				new_s = g_score[current] + dist

				if (new_s < g_score[neighbor]):
					parent[neighbor] = current
					g_score[neighbor] = new_s
					f_score[neighbor] = g_score[neighbor] + self.cost_estimate(neighbor, dest_node)
					if not open_set_keys[neighbor]:	
						open_set_keys[neighbor] = True
						heappush(openset, (f_score[neighbor], neighbor))

		return []
		
	def get_path(self, parent, source_node, dest_node):
		result = []
		while(parent[dest_node] != None):
			result.append(dest_node)
			dest_node = parent[dest_node]
		result.append(source_node)

		return result[::-1]

# g = Graph()
# g.load_data("path/path.data")
# print("done")
# start = time.clock()
# g.apply_a_star(0,100)
# print time.clock() - start