import global_vars
import pqueue

global graph

def dijkstra(start, user):
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
	while Q:
		v = Q.pop()
		if v in user.node_rating_dict:
			rating = user.node_rating_dict[v]
			current = v
			confidence = 1
			length_of_path = 0
			while current is not start:
				rating += graph.edge_matrix[current, prev[current]].mean_of_diffs
				confidence *= graph.edge_matrix[current, prev[current]].confidence
				length_of_path += 1
				current = prev[current]
			best_rating_so_far = (abs(rating - 50), start)
			for node in same_item_nodes:
				if abs(rating + graph.edge_matrix[start][node].mean_of_diffs - 50) < best_rating_so_far[0]:
					best_rating_so_far = (rating + graph.edge_matrix[start][node].mean_of_diffs - 50, node)
			if best_rating_so_far[1] == start:
				return (best_rating_so_far[1], best_rating_so_far[0], confidence, length_of_path)
			return (best_rating_so_far[1], best_rating_so_far[0], confidence*graph.edge_matrix[start][best_rating_so_far[1].confidence, length_of_path)
		for neighbor in graph.neighbors_lst[v]:
			if dist[neighbor] > dist[v] + graph.edge_matrix[v][neighbor].cost and neighbor not in same_item_nodes:
				dist[neighbor] = dist[v] + graph.edge_matrix[v][neighbor].cost
				Q.push(neighbor, dist[neighbor])
				prev[neighbor] = v

