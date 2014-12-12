from global_vars import graph
import pqueue
import time

global graph

# normal unidirectional UCS
def dijkstra(user, start):
	dist = {}
	prev = {}
	# list of different sizes of the same node as start
	same_item_nodes = graph.get_same_nodes(start)
	# initialize all costs to infinity except start
	for node in graph.neighbors_lst:
		dist[node] = float("inf")
	dist[start] = 0
	Q = pqueue.PriorityQueue()
	Q.push(start, 0)
	expanded = 0
	# while there are still nodes to be popped
	while not Q.is_empty():
		v = Q.pop()
		# increment the number of expanded nodes
		expanded += 1
		# if node has already been purchased by user (stop condition)
		if v in user.node_rating_dict:
			rating = user.node_rating_dict[v]
			current = v
			confidence = 1
			length_of_path = 0
			# aggregate confidences and ratings across path
			while current is not start:
				rating += graph.edge_matrix[current][prev[current]].mean_of_diffs
				confidence *= graph.edge_matrix[current][prev[current]].confidence
				length_of_path += 1
				current = prev[current]
			# pick size of start item that would have best rating (closest to 50), update confidence if necessary (multiply by 0.7: confidence of fake edge)	
			best_rating_so_far = rating
			best_diff_so_far = (abs(rating - 50), start)
			for node in same_item_nodes:
				if abs(rating + graph.edge_matrix[start][node].mean_of_diffs - 50) < best_diff_so_far[0]:
					best_diff_so_far = (rating + graph.edge_matrix[start][node].mean_of_diffs - 50, node)
					best_rating_so_far = rating + graph.edge_matrix[start][node].mean_of_diffs
			if best_diff_so_far[1] == start:
				return (best_diff_so_far[1], best_rating_so_far, confidence, length_of_path, expanded)
			return (best_diff_so_far[1], best_rating_so_far, confidence*graph.edge_matrix[start][best_diff_so_far[1]].confidence, length_of_path+1, expanded)
		# push node on heap if appropriate, unless node is same item as the start node
		for neighbor in graph.neighbors_lst[v]:
			if dist[neighbor] > dist[v] + graph.edge_matrix[v][neighbor].cost and neighbor not in same_item_nodes:
				dist[neighbor] = dist[v] + graph.edge_matrix[v][neighbor].cost
				Q.push(neighbor, dist[neighbor])
				prev[neighbor] = v





# start queue has to not be empty, and at least one of the end queues has to not be empty
def while_condition(queueStart, queueEnds):
	if queueStart.is_empty():
		return False
	for queueEnd in queueEnds:
		if not queueEnd.is_empty():
			return True
	return False
 
# no end queue must have a minimum cost lower than best_path - start queue's minimum
def stop_condition(queueStart, queueEnds, best_path):
	for queueEnd in queueEnds:
		if queueStart.heap[0][0] + queueEnd.heap[0][0] <= best_path:
			return False
	return True

# K-directional UCS
def kdirectionalDijkstra(user, start):
	# initialize K arrays, dicts and goals, one for each goal
	prevEnds = [None for i in range(len(user.node_rating_dict))]
	distEnds = [None for i in range(len(user.node_rating_dict))]
	visitedEnds = [None for i in range(len(user.node_rating_dict))]
	queueEnds = [None for i in range(len(user.node_rating_dict))]
	goals = list(user.node_rating_dict.keys())
	for i in range(len(user.node_rating_dict)):
		prevEnds[i] = {}
		distEnds[i] = {}
		visitedEnds[i] = {}
		for node in graph.neighbors_lst:
			distEnds[i][node] = float('inf')
		distEnds[i][goals[i]] = 0
		queueEnds[i] = pqueue.PriorityQueue()
		queueEnds[i].push(goals[i], 0)

	#initialize start
	distStart = {}
	visitedStart = {}
	nodesExpanded = 0
	intersection = None
	best_path = float("inf")
	for node in graph.neighbors_lst:
		distStart[node] = float('inf')

	prevStart = {}
	distStart[start] = 0
	queueStart = pqueue.PriorityQueue()
	queueStart.push(start, 0)

	same_item_nodes = graph.get_same_nodes(start)
	while while_condition(queueStart, queueEnds):
		if stop_condition(queueStart, queueEnds, best_path):
			rating = user.node_rating_dict[goals[intersection[1]]]
			confidence = 1
			length_of_path = 0
			if intersection is None:
				raise ValueError("intersection is None")

			current = intersection[0]
			# aggregate ratings and confidences across both sides of path
			while current is not start:
				rating += graph.edge_matrix[current][prevStart[current]].mean_of_diffs
				confidence *= graph.edge_matrix[current][prevStart[current]].confidence
				length_of_path += 1
				current = prevStart[current]
			current = intersection[0]
			i = intersection[1]
			while current is not goals[i]:
				rating -= graph.edge_matrix[current][prevEnds[i][current]].mean_of_diffs
				confidence *= graph.edge_matrix[current][prevEnds[i][current]].confidence
				length_of_path += 1
				current = prevEnds[i][current]
			# pick size with best rating (just like UCS)
			best_rating_so_far = rating
			best_diff_so_far = (abs(rating - 50), start)
			for node in same_item_nodes:
				if abs(rating + graph.edge_matrix[start][node].mean_of_diffs - 50) < best_diff_so_far[0]:
					best_diff_so_far = (rating + graph.edge_matrix[start][node].mean_of_diffs - 50, node)
					best_rating_so_far = rating + graph.edge_matrix[start][node].mean_of_diffs

			if best_diff_so_far[1] == start:
				return (best_diff_so_far[1], best_rating_so_far, confidence, length_of_path, nodesExpanded)
			return (best_diff_so_far[1], best_rating_so_far, confidence*graph.edge_matrix[start][best_diff_so_far[1]].confidence, length_of_path+1, nodesExpanded)

		# expand from start's side
		v = queueStart.pop()
		visitedStart[v] = True
		nodesExpanded += 1
		for neighbor in graph.neighbors_lst[v]:
			# normal UCS code
			if distStart[neighbor] > distStart[v] + graph.edge_matrix[v][neighbor].cost and neighbor not in same_item_nodes:
					distStart[neighbor] = distStart[v] + graph.edge_matrix[v][neighbor].cost
					queueStart.push(neighbor, distStart[neighbor])
					prevStart[neighbor] = v
			for i in range(len(visitedEnds)):
				# if there is intersection
				if neighbor in visitedEnds[i]:
					if(best_path > distStart[v] + graph.edge_matrix[v][neighbor].cost + distEnds[i][neighbor] and neighbor not in same_item_nodes):
						best_path = distStart[v] + graph.edge_matrix[v][neighbor].cost + distEnds[i][neighbor]
						intersection = (neighbor, i)
						prevStart[neighbor] = v
		# expand from every goal's side
		for i in range(len(visitedEnds)):
			u = queueEnds[i].pop()
			visitedEnds[i][u] = True
			nodesExpanded +=1
			for neighbor in graph.neighbors_lst[u]:
				if neighbor in visitedStart:
					if(best_path > distEnds[i][u] + graph.edge_matrix[u][neighbor].cost + distStart[neighbor] and neighbor not in same_item_nodes):
						best_path = distEnds[i][u] + graph.edge_matrix[u][neighbor].cost + distStart[neighbor]
						intersection = (neighbor, i)
						prevEnds[i][neighbor] = u
				if distEnds[i][neighbor] > distEnds[i][u] + graph.edge_matrix[u][neighbor].cost and neighbor not in same_item_nodes:
					distEnds[i][neighbor] = distEnds[i][u] + graph.edge_matrix[u][neighbor].cost
					queueEnds[i].push(neighbor, distEnds[i][neighbor])
					prevEnds[i][neighbor] = u\





