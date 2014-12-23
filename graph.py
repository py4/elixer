from heapq import *
import sys

class Graph:

	def __init__(self):
		self.list = []
		self.nodes_count = 0
		self.edges_count = 0
		self.nodes_dict = {}
		self.reverse_nodes_dict = []
		self.cache = {}

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
				# print("===============================")
				# print("node_id:  ", current_node_id)
				# print("x,y:  ", self.reverse_nodes_dict[current_node_id])
				# print("neighbor_id:  ", node_id)
				# print("x,y of neighbor:  ", self.reverse_nodes_dict[node_id])
				# print("weight:  ", weight)
				# print("===============================")

	def apply_dijkstra(self, source_node, dest_node):
		if(len(self.list[source_node]) == 0):
			self.cache = {}
			print(" --- !!!! --- this node does not have any out degre")
			return []

		rep = self.get_cache_rep()
	
		if(rep == source_node):
			print "reading from cache!"
			result = self.get_path(self.cache[rep], source_node, dest_node)
			if(len(result) == 1):
				c = 0
				al = 0
				for el in self.cache[rep]:
					if(el == None):
						c += 1
					al += 1
				print("c:  ", c)
				print("all:  ", al)
			return result

		# print("source_node:  ", source_node)
		# print("dest_node:  ", dest_node)
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

		fuck = False
		while len(queue) > 0:
			dist_u,u = heappop(queue)
			# if(u == dest_node):
			# 	break
			for v,w in self.list[u]:
				alt = dist[u] + w
				#print("fucking alt:  ", alt)
				#print("fucking dist[v]:  ", dist[v])
				if(alt < dist[v]):
					dist[v] = alt
					parent[v] = u
					heappush(queue, (dist[v], v))
					fuck = True

		print ("###### DIJSKTRA LOG ##########")
		c = 0
		al = 0
		for el in parent:
			if(el == None):
				c += 1
		 	al += 1
		print("None items:  ", c)
		print("all items:  ", al)
		print("#################################")

		if not fuck:
			print("############################3")
			print("############################3")
			print("THIS IS FUCK!!!!")
			print("############################3")
			print("############################3")
			sys.exit()

		self.cache = {}		
		self.cache[source_node] = parent
		return self.get_path(parent, source_node, dest_node)
#		result.append(dest_node)
		

		# print ("fucking result:  ", result[::-1])
		# return result[::-1]

	def get_path(self, parent, source_node, dest_node):
		result = []
		while(parent[dest_node] != None):
			result.append(dest_node)
			dest_node = parent[dest_node]
		result.append(source_node)

		# if(len(result) == 1):
		# 	print(parent)
		return result[::-1]

#self.graph.apply_dijkstra(self.graph.nodes_dict[source], self.graph.nodes_dict[destination])

# g = Graph()
# g.load_data("path/path.data")
# g.apply_dijkstra(g.nodes_dict[(550753.0, 3935390.0)],g.nodes_dict[(542063.0, 3939030.0)])