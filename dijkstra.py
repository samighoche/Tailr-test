from global_vars import graph
import pqueue

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
			print(expanded)
			rating = user.node_rating_dict[v]
			current = v
			confidence = 1
			length_of_path = 0
			while current is not start:
				print(graph.edge_matrix[current][prev[current]])
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
				return (best_diff_so_far[1], best_rating_so_far, confidence, length_of_path)
			return (best_diff_so_far[1], best_rating_so_far, confidence*graph.edge_matrix[start][best_diff_so_far[1]].confidence, length_of_path)
		for neighbor in graph.neighbors_lst[v]:
			if dist[neighbor] > dist[v] + graph.edge_matrix[v][neighbor].cost and neighbor not in same_item_nodes:
				dist[neighbor] = dist[v] + graph.edge_matrix[v][neighbor].cost
				Q.push(neighbor, dist[neighbor])
				prev[neighbor] = v


