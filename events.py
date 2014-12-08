import infrastructure
import global_vars
from dijkstra import bidirectional_uniform_cost_search
from PS import perimeter_search
from LS import beam_search

def ask_for_prediction_dijkstra(user, node):
	if node in user.node_rating_dict:
		return user.node_rating_dict[node]
	else:
		return bidirectional_uniform_cost_search(user, node)

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
	global graph
	user.rate_node(node, rating)
	for previous_purchase in user.node_rating_dict:
		# if edge doesn't already exist
		diff = user.get_node_rating(node) - user.get_node_rating(previous_purchase)
		if graph.is_new_edge(node, previous_purchase):
			graph.add_edge(node, previous_purchase)
		graph.update_edge(node, previous_purchase, -diff)
		graph.update_edge(previous_purchase, node, diff)

