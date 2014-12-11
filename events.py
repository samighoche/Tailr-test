import infrastructure
import global_vars
from global_vars import graph
from dijkstra import dijkstra
from dijkstra import bidirectionalDijkstra
from astar import astar
# from PS import perimeter_search
# from LS import beam_search


def ask_for_prediction_dijkstra(user, node):
	result = dijkstra(user, node)
	if result is None:
		print("No path exists")
	else:
		(best_node, predicted_rating, confidence, length_of_path) = result
		print("best_node: ", best_node, " predicted_rating: ", predicted_rating, " confidence: ", confidence, " length_of_path: ", length_of_path)

def ask_for_prediction_astar(user, node):
	result = astar(user, node)
	if result is None:
		print("No path exists")
	else:
		(best_node, predicted_rating, confidence, length_of_path) = result
		print("best_node: ", best_node, " predicted_rating: ", predicted_rating, " confidence: ", confidence, " length_of_path: ", length_of_path)

def ask_for_prediction_perimeter_search(user, node):
	if node in user.node_rating_dict:
		return user.node_rating_dict[node]
	else:
		return perimeter_search(user, node)


def ask_for_prediction_bidirectional(start, goal, user):
	result = bidirectionalDijkstra(start, goal, user)
	print result


def ask_for_prediction_beam_search(user, node):
	if node in user.node_rating_dict:
		return user.node_rating_dict[node]
	else:
		return beam_search(user, node)


def rate_event(user, node, rating):
	global graph
	for previous_purchase in user.node_rating_dict:
		# if edge doesn't already exist
		diff = rating - user.get_node_rating(previous_purchase)
		if graph.is_new_edge(node, previous_purchase):
			graph.add_edge(node, previous_purchase)
			global_vars.num_edges += 1
		graph.update_edge(node, previous_purchase, -diff)
		graph.update_edge(previous_purchase, node, diff)
	user.rate_node(node, rating)
	

