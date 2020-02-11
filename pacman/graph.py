import math
from collections import defaultdict
from pacman_utils import add, Direction

	
class Graph: 
	def __init__(self, nodes):
		self.graph = defaultdict(list)
		for node in nodes:
			adjacent_nodes = [add(node, d.value) for d in Direction if add(node, d.value) in nodes]
			for adjacent_node in adjacent_nodes:
				self.add_edge(node, adjacent_node)

	def add_edge(self, u, v):
		self.graph[u].append(v)

	def delete_node(self, node):
		if node in self.graph:
			for adjacent_node in self.graph[node]:
				self.graph[adjacent_node].remove(node)
			self.graph.pop(node)
		else:
			pass

	def shortest_path(self, source, destination):
		shortest_path = [destination]
		predecessor, _ = self.BFS(source, destination)
		i = destination
		while predecessor[i] != -1:
			# print(predecessor[i])
			shortest_path.append(predecessor[i])
			i = predecessor[i]
		shortest_path.reverse()
		return shortest_path

	def BFS(self, source, destination): 
		# Create a queue for BFS 
		queue = []

		# Initially, all nodes are unvisited. The distance to each node is set to infinity
		visited = {}
		distance = {}
		predecessor = {}
		for node in self.graph:
			visited[node] = False
			distance[node] = math.inf
			predecessor[node] = -1

		# Mark the source node as visited and enqueue it 
		queue.append(source)
		visited[source] = True
		distance[source] = 0

		# Standard BFS algorithm
		while queue:  
			# Dequeue a node from the queue
			s = queue.pop(0)

			# Enqueue all unvisited adjacent nodes of the dequeued node s
			for adjacent_node in self.graph[s]:
				if visited[adjacent_node] == False: 
					queue.append(adjacent_node) 
					visited[adjacent_node] = True
					distance[adjacent_node] = distance[s] + 1
					predecessor[adjacent_node] = s
					if adjacent_node == destination:
						# The destionation node is reachable from the source node
						return predecessor, distance 
			
		# The destionation node is NOT reachable from the source node
		return None, None	
