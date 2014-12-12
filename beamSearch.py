##################################################
# 											     #
# http://en.wikipedia.org/wiki/Quickselect		 #									 
#												 #
##################################################

from random import randint
from infrastructure import *
from global_vars import *
from collections import deque

global graph
beamSize = 10

# helper function that swaps 2 elements in a list
def swap (lst,index1,index2):
	temp = lst[index1]
	lst[index1] = lst[index2]
	lst[index2] = temp

# helper function that returns cost between 2 nodes
def cost((node1,node2)):
	return graph.edge_matrix[node1][node2].cost

# partitions a list of nodes around a given cost
def partition(lst,left,right,pivotIndex):
	pivot = cost(lst[pivotIndex])
	swap (lst, pivotIndex,right)
	storeIndex = left
	for i in range (left,right):
		if cost(lst[i]) < pivot:
			swap (lst,storeIndex,i)
			storeIndex += 1
	swap (lst,right,storeIndex)
	return storeIndex

# quickselects the n nodes with the lowest cost 
# (highest confidence) drop from a list of items
def select(lst,left,right,n):

	output = []

	if left == right:
		for index in xrange(left):
			output.append(lst[index])
		return output

	pivotIndex = randint(left,right)
	pivotIndex = partition(lst,left,right,pivotIndex)

	if n == pivotIndex:
		for index in xrange(n):
			output.append(lst[index])
		return output
	elif n < pivotIndex:
		return select(lst,left,pivotIndex -1,n)
	else:
		return select(lst,pivotIndex+1,right,n)

# beam search algorithm
def beam_search(user,item):

	expanded = 0
	goal_set = user.node_rating_dict
	root = item
	prev = {}
	visited = {}
	# create beam and append root to it
	beam = deque([(item,None)])

	# create temporary queue
	q = deque()

	# create list of all sizes of 'item'
	same_item_nodes = []
	for node in graph.neighbors_lst[root]:
		if graph.edge_matrix[root][node].same_item:
			same_item_nodes.append(node)

	# while beam queue is not empty
	while beam != deque():
		#increment number of expanded nodes
		expanded += 1

		#pop leftmost element from beam
		v,p = beam.popleft()
		visited[v] = True
		# store popped element's predecessor to reconstruct path
		# from goal to start item when a goal is found
		prev[v] = p

		# expand popped node
		for neighbor in graph.get_neighbors(v):
			if neighbor in goal_set:
				# reconstruct path to root (item to buy)
				prev[neighbor] = v
				v = neighbor
				rating = user.node_rating_dict[v]
				current = v
				confidence = 1
				length_of_path = 0
				while current is not root:
					rating += graph.edge_matrix[current][prev[current]].mean_of_diffs
					confidence *= graph.edge_matrix[current][prev[current]].confidence
					length_of_path += 1
					current = prev[current]
				best_rating_so_far = rating
				best_diff_so_far = (abs(rating - 50), root)
				for node in same_item_nodes:
					if abs(rating + graph.edge_matrix[root][node].mean_of_diffs - 50) < best_diff_so_far[0]:
						best_diff_so_far = (rating + graph.edge_matrix[root][node].mean_of_diffs - 50, node)
						best_rating_so_far = rating + graph.edge_matrix[root][node].mean_of_diffs
				if best_diff_so_far[1] == root:
					return (best_diff_so_far[1], best_rating_so_far, confidence, length_of_path, expanded)
				return (best_diff_so_far[1],best_rating_so_far, confidence*graph.edge_matrix[root][best_diff_so_far[1]].confidence, length_of_path, expanded)

			# if neighor is not the start node and is not the same item than
			# popped node, add it to temp queue
			if neighbor != root and not graph.edge_matrix[v][neighbor].same_item and neighbor not in visited:
				q.append((neighbor,v))

		# if all elements were popped off the beam
		if beam == deque():
			# if temp queue is larger then beamSize
			if len(q) > beamSize:
				# select k nodes with highest confidence from temp queue
				beam = deque(select(q,0,len(q) - 1,beamSize))
			else:
				beam = q
			# reset temp queue for next beam iteration
			q = deque()

