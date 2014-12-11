import infrastructure
import global_vars
from global_vars import graph
from dijkstra import dijkstra
from dijkstra import bidirectionalDijkstra
from astar import astar
# from PS import perimeter_search
# from LS import beam_search

global graph

def ask_for_prediction(algorithm, user, node):
	same_nodes = graph.get_same_nodes(node)
	same_nodes.append(node)
	max_conf = None
	best_result = None
	for node in same_nodes:
		if algorithm == "dijkstra":
			result = dijkstra(user, node)
		elif algorithm == "astar":
			result = astar(user, node)
		elif algorithm == "bidirectional":
		  	max_conf_for_size = None
			best_result_for_size = None
			for goal in user.node_rating_dict:
			  result = bidirectionalDijkstra(node, goal, user)
			  if result is not None:
			  	if best_result_for_size is None or result[2] > max_conf_for_size:
			  		max_conf_for_size = result[2]
			  		best_result_for_size = result
			result = best_result_for_size
		if result is not None:
			if best_result is None or result[2] > max_conf:
				max_conf = result[2]
				best_result = result
	if best_result is None:
		print("Path does not exist")
	else:
		(best_node, predicted_rating, confidence, length_of_path, expanded) = best_result
		print("best_node: ", best_node, " predicted_rating: ", predicted_rating, " confidence: ", confidence, " length_of_path: ", length_of_path, " expanded nodes: ", expanded)


def ask_for_prediction_perimeter_search(user, node):
	if node in user.node_rating_dict:
		return user.node_rating_dict[node]
	else:
		return perimeter_search(user, node)



def ask_for_prediction_beam_search(user, node):
	if node in user.node_rating_dict:
		return user.node_rating_dict[node]
	else:
		return beam_search(user, node)


def rate_event(user, node, rating):
	
	for previous_purchase in user.node_rating_dict:
		# if edge doesn't already exist
		diff = rating - user.get_node_rating(previous_purchase)
		if graph.is_new_edge(node, previous_purchase):
			graph.add_edge(node, previous_purchase)
			global_vars.num_edges += 1
		graph.update_edge(node, previous_purchase, -diff)
		graph.update_edge(previous_purchase, node, diff)
	user.rate_node(node, rating)
	

