from global_vars import graph
import global_vars
import pqueue

global graph

# heuristic that depends on number of outgoing edges, 
# and correlation of brands, basically preferring nodes from brands that might lead
# to a goal's brand
def heuristic(user, node):
	num_outgoing_edges = len(graph.neighbors_lst[node])
	num_goal_nodes = len(user.node_rating_dict)
	total = 0
	for brand in user.brand_list:
		if brand in graph.brand_matrix[node.brand]:
			total += user.brand_list[brand]*graph.brand_matrix[node.brand][brand]
	correlation_average = total/num_goal_nodes
	return num_outgoing_edges/80 + 0.3*correlation_average/global_vars.num_edges

# heuristic that depends on number of edges,
# and correlation of brands, basically preferring nodes from brands that match one of the goals' brand
# def heuristic(user, node):
# 	num_outgoing_edges = len(graph.neighbors_lst[node])
# 	num_goal_nodes = len(user.node_rating_dict)
# 	brandadd = 0
# 	for brand in user.brand_list:
# 		if brand == node.brand:
# 			brandadd = user.brand_list[brand]*0.01
# 	return num_outgoing_edges/100 + brandadd


# start queue has to not be empty, and at least one of the end queues has to not be empty
def while_condition(queueStart, queueEnds):
	if queueStart.is_empty():
		return False
	for queueEnd in queueEnds:
		if not queueEnd.is_empty():
			return True
	return False

def perimeter_search(user, start, limit):
	# initialize goal sides' arrays, dicts, queues
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

	# initialize start side
	distStart = {}
	visitedStart = {}
	nodesExpanded = 0
	intersection = None
	best_path = float("inf")
	for node in graph.neighbors_lst:
		distStart[node] = float('inf')

	prevStart = {}
	distStart[start] = 0
	g = {}
	g[start] = 0
	queueStart = pqueue.PriorityQueue()
	queueStart.push(start, 0)

	same_item_nodes = graph.get_same_nodes(start)

	while while_condition(queueStart, queueEnds):
		# if have already found a path, greedily take it
		if best_path != float("inf"):
			rating = user.node_rating_dict[goals[intersection[1]]]
			confidence = 1
			length_of_path = 0
			if intersection is None:
				raise ValueError("intersection is None")

			current = intersection[0]
			# aggregate ratings and confidences across path
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
			# decide whether to take a fake edge from the start or not (just like UCS)
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
			g[neighbor] = g[v] + graph.edge_matrix[v][neighbor].cost
			if distStart[neighbor] > g[neighbor] + heuristic(user, neighbor) and neighbor not in same_item_nodes:
				distStart[neighbor] = g[neighbor] + heuristic(user, neighbor)
				queueStart.push(neighbor, distStart[neighbor])
				prevStart[neighbor] = v
			for i in range(len(visitedEnds)):
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
				# make sure to never push anything on the queue if it has a cost higher than the threshold of perimeter search
				if distEnds[i][neighbor] > distEnds[i][u] + graph.edge_matrix[u][neighbor].cost and distEnds[i][u] + graph.edge_matrix[u][neighbor].cost <= limit and neighbor not in same_item_nodes:
					distEnds[i][neighbor] = distEnds[i][u] + graph.edge_matrix[u][neighbor].cost
					queueEnds[i].push(neighbor, distEnds[i][neighbor])
					prevEnds[i][neighbor] = u





