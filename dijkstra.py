from global_vars import graph
import pqueue
import time

global graph

def dijkstra(user, start):
	dist = {}
	prev = {}
	same_item_nodes = []
	for node in graph.neighbors_lst[start]:
		if graph.edge_matrix[start][node].same_item:
			same_item_nodes.append(node)
	for node in graph.neighbors_lst:
		dist[node] = float("inf")
	dist[start] = 0
	Q = pqueue.PriorityQueue()
	Q.push(start, 0)
	expanded = 0
	while not Q.is_empty():
		v = Q.pop()
		expanded += 1
		if v in user.node_rating_dict:
			# print(expanded)
			rating = user.node_rating_dict[v]
			current = v
			confidence = 1
			length_of_path = 0
			while current is not start:
				# print(graph.edge_matrix[current][prev[current]])
				rating += graph.edge_matrix[current][prev[current]].mean_of_diffs
				confidence *= graph.edge_matrix[current][prev[current]].confidence
				length_of_path += 1
				current = prev[current]
			best_rating_so_far = rating
			best_diff_so_far = (abs(rating - 50), start)
			for node in same_item_nodes:
				if abs(rating + graph.edge_matrix[start][node].mean_of_diffs - 50) < best_diff_so_far[0]:
					best_diff_so_far = (rating + graph.edge_matrix[start][node].mean_of_diffs - 50, node)
					best_rating_so_far = rating + graph.edge_matrix[start][node].mean_of_diffs

			# print("best_diff_so_far: ", svasdvadvas, " goal's size: ", v.size)
			if best_diff_so_far[1] == start:
				print((best_diff_so_far[1], best_rating_so_far, confidence, length_of_path, expanded))
				return (best_diff_so_far[1], best_rating_so_far, confidence, length_of_path, expanded)
			print((best_diff_so_far[1], best_rating_so_far, confidence*graph.edge_matrix[start][best_diff_so_far[1]].confidence, length_of_path+1, expanded))
			return (best_diff_so_far[1], best_rating_so_far, confidence*graph.edge_matrix[start][best_diff_so_far[1]].confidence, length_of_path+1, expanded)
		for neighbor in graph.neighbors_lst[v]:
			if dist[neighbor] > dist[v] + graph.edge_matrix[v][neighbor].cost and neighbor not in same_item_nodes:
				dist[neighbor] = dist[v] + graph.edge_matrix[v][neighbor].cost
				Q.push(neighbor, dist[neighbor])
				prev[neighbor] = v



def bidirectionalDijkstra(start, goal, user):
	distStart = {}
	prevStart = {}
	distEnd = {}
	prevEnd = {}
	forwardEnd = {}
	same_item_nodes = []

	best_path = float('inf')

	visitedStart = {}
	visitedGoal = {}
	nodesExpanded = 0
	intersection = None

	for node in graph.neighbors_lst[start]:
		if graph.edge_matrix[start][node].same_item:
			same_item_nodes.append(node)

	for node in graph.neighbors_lst:
		distStart[node] = float('inf')
		distEnd[node] = float('inf')

	distStart[start] = 0
	distEnd[goal] = 0

	queueStart = pqueue.PriorityQueue()
	queueStart.push(start, 0)

	queueEnd = pqueue.PriorityQueue()
	queueEnd.push(goal, 0)

	while not (queueStart.is_empty() or queueEnd.is_empty()):

		
		if(queueStart.heap[0][0] + queueEnd.heap[0][0] > best_path):
			rating = user.node_rating_dict[goal]
			confidence = 1
			length_of_path = 0
			current = intersection
			if current is None:
				raise ValueError("intersection is None")

			while current is not start:
				rating += graph.edge_matrix[current][prevStart[current]].mean_of_diffs
				confidence *= graph.edge_matrix[current][prevStart[current]].confidence
				length_of_path += 1
				current = prevStart[current]
			current = intersection
			while current is not goal:
				rating -= graph.edge_matrix[current][prevEnd[current]].mean_of_diffs
				confidence *= graph.edge_matrix[current][prevEnd[current]].confidence
				length_of_path += 1
				current = prevEnd[current]
			
			best_rating_so_far = rating
			best_diff_so_far = (abs(rating - 50), start)
			for node in same_item_nodes:
				if abs(rating + graph.edge_matrix[start][node].mean_of_diffs - 50) < best_diff_so_far[0]:
					best_diff_so_far = (rating + graph.edge_matrix[start][node].mean_of_diffs - 50, node)
					best_rating_so_far = rating + graph.edge_matrix[start][node].mean_of_diffs

			# print("best_diff_so_far: ", svasdvadvas, " goal's size: ", v.size)
			if best_diff_so_far[1] == start:
				print((best_diff_so_far[1], best_rating_so_far, confidence, length_of_path, nodesExpanded))
				return (best_diff_so_far[1], best_rating_so_far, confidence, length_of_path, nodesExpanded)
			print((best_diff_so_far[1], best_rating_so_far, confidence*graph.edge_matrix[start][best_diff_so_far[1]].confidence, length_of_path+1, nodesExpanded))
			return (best_diff_so_far[1], best_rating_so_far, confidence*graph.edge_matrix[start][best_diff_so_far[1]].confidence, length_of_path+1, nodesExpanded)

		v = queueStart.pop()
		visitedStart[v] = True
		nodesExpanded += 1

		for neighbor in graph.neighbors_lst[v]:
			if(neighbor in visitedGoal):
				if(best_path > distStart[v] + graph.edge_matrix[v][neighbor].cost + distEnd[neighbor] and neighbor not in same_item_nodes):
					best_path = distStart[v] + graph.edge_matrix[v][neighbor].cost + distEnd[neighbor]
					intersection = neighbor
					prevStart[neighbor] = v
			else:
				pass

			if distStart[neighbor] > distStart[v] + graph.edge_matrix[v][neighbor].cost and neighbor not in same_item_nodes:
				distStart[neighbor] = distStart[v] + graph.edge_matrix[v][neighbor].cost
				queueStart.push(neighbor, distStart[neighbor])
				prevStart[neighbor] = v

		u = queueEnd.pop()
		visitedGoal[u] = True
		nodesExpanded +=1

		for neighbor in graph.neighbors_lst[u]:
			if(neighbor in visitedStart):
				
				if(best_path > distEnd[u] + graph.edge_matrix[u][neighbor].cost + distStart[neighbor] and neighbor not in same_item_nodes):
					best_path = distEnd[u] + graph.edge_matrix[u][neighbor].cost + distStart[neighbor]
					intersection = neighbor
					prevEnd[neighbor] = u
			else:
				pass

			if distEnd[neighbor] > distEnd[u] + graph.edge_matrix[u][neighbor].cost and neighbor not in same_item_nodes:
				distEnd[neighbor] = distEnd[u] + graph.edge_matrix[u][neighbor].cost
				queueEnd.push(neighbor, distEnd[neighbor])
				prevEnd[neighbor] = u


