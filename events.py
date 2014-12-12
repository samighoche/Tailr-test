import infrastructure
import global_vars
from global_vars import graph
from dijkstra import dijkstra
from dijkstra import bidirectionalDijkstra
from dijkstra import kdirectionalDijkstra
from astar import astar
from perimeter import perimeter_search
from beamSearch import beam_search
# from PS import perimeter_search
# from LS import beam_search

global graph

def ask_for_prediction(algorithm, user, node, limit=None):
	same_nodes = graph.get_same_nodes(node)
	same_nodes.append(node)
	max_conf = None
	best_result = None
	result = None
	expanded = 0
	for node in same_nodes:
		if algorithm == "dijkstra":
			result = dijkstra(user, node)
			if result is not None:
				expanded += result[4]
		elif algorithm == "astar":
			result = astar(user, node)
			if result is not None:
				expanded += result[4]
		elif algorithm == "kdirectional":
			result = kdirectionalDijkstra(user, node)
			if result is not None:
				expanded += result[4]
		elif algorithm == "perimeter_search":
			result = perimeter_search(user, node, limit)
			if result is not None:
				expanded += result[4]
		elif algorithm == "beam_search":
			result = beam_search(user, node)
			if result is not None:
				expanded += result[4]
		if result is not None:
			if best_result is None or result[2] > max_conf:
				max_conf = result[2]
				best_result = result
	if best_result is None:
		print("Path does not exist")
	else:
		(best_node, predicted_rating, confidence, length_of_path, _) = best_result
		print("best_node: ", best_node, " predicted_rating: ", predicted_rating, " confidence: ", confidence, " length_of_path: ", length_of_path, " expanded nodes: ", expanded)



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
	

