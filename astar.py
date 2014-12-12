from global_vars import graph
import global_vars
import pqueue

global graph

# def heuristic(user, node):
# 	num_outgoing_edges = len(graph.neighbors_lst[node])
# 	num_goal_nodes = len(user.node_rating_dict)
# 	total = 0
# 	for brand in user.brand_list:
# 		if brand in graph.brand_matrix[node.brand]:
# 			total += user.brand_list[brand]*graph.brand_matrix[node.brand][brand]
# 	correlation_average = total/num_goal_nodes
# 	return num_outgoing_edges/80 + 0.3*correlation_average/global_vars.num_edges

def heuristic(user, node):
	num_outgoing_edges = len(graph.neighbors_lst[node])
	num_goal_nodes = len(user.node_rating_dict)
	brandadd = 0
	for brand in user.brand_list:
		if brand == node.brand:
			brandadd = user.brand_list[brand]*0.01
	return num_outgoing_edges/100 + brandadd


def astar(user, start):
	g = {}
	f = {}
	prev = {}
	same_item_nodes = []
	for node in graph.neighbors_lst[start]:
		if graph.edge_matrix[start][node].same_item:
			same_item_nodes.append(node)
	for node in graph.neighbors_lst:
		f[node] = float("inf")
	f[start] = 0
	g[start] = 0
	Q = pqueue.PriorityQueue()
	Q.push(start, 0)
	expanded = 0
	while not Q.is_empty():
		v = Q.pop()
		expanded += 1
		if v in user.node_rating_dict:
			rating = user.node_rating_dict[v]
			current = v
			confidence = 1
			length_of_path = 0
			while current is not start:
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
			if best_diff_so_far[1] == start:
				return (best_diff_so_far[1], best_rating_so_far, confidence, length_of_path, expanded)
			return (best_diff_so_far[1], best_rating_so_far, confidence*graph.edge_matrix[start][best_diff_so_far[1]].confidence, length_of_path+1, expanded)
		for neighbor in graph.neighbors_lst[v]:
			g[neighbor] = g[v] + graph.edge_matrix[v][neighbor].cost
			if f[neighbor] > g[neighbor] + heuristic(user, neighbor) and neighbor not in same_item_nodes:
				f[neighbor] = g[neighbor] + heuristic(user, neighbor)
				Q.push(neighbor, f[neighbor])
				prev[neighbor] = v