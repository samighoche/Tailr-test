from global_vars import current_user_id, current_item_id, graph
import infrastructure
import random
import events
import math

num_users = 400
num_items = 1100
num_purchases = 3000
num_brands = 8
nodes_per_item = 3

users_list = [None for i in range(num_users)]
nodes_list = [None for i in range(num_items*nodes_per_item)]
brands_list = [None for i in range(num_brands)]
global graph

# create list of users
def initialize_users():
  for i in range(num_users):
    true_size = random.randint(30,70)
    global current_user_id
    user = infrastructure.User(true_size, current_user_id)
    current_user_id += 1
    users_list[i] = user

# create list of items with random brands, create different (and random) sizes for each item
def initialize_items():
  for i in range(num_items):
    same_items = []
    for j in range(nodes_per_item):
      # GOTTA FIX THIS HERE
      size = random.randint(30+j*10, 70-(nodes_per_item-j)*10)
      global current_item_id
      brand_index = random.randint(0, num_brands-1)
      brand = brands_list[brand_index]
      if brand not in graph.brand_matrix:
        graph.brand_matrix[brand] = {}
      node = infrastructure.Node(size, current_item_id, brand)
      current_item_id += 1
      graph.add_node(node)
      for other_size in same_items:
        graph.add_edge(node, other_size, True)
      same_items.append(node)
      nodes_list[i*nodes_per_item+j] = node

# create brands  
def initialize_brands():
  for i in range(num_brands):
    brands_list[i] = "brand" + str(i)

# check if node's clothing item has already been purchased by user (perhaps a different size of it)
def is_same_as_already_purchased_item(user, node):
  for purchase in user.node_rating_dict:
    if node in graph.edge_matrix[purchase] and graph.edge_matrix[purchase][node].same_item:
      return True
  return False


# simulate purchases
def make_purchases(num_purchases):
  i = 0
  while i < num_purchases:
    # pick a random user
    userid = random.randint(0, num_users-1)
    user = users_list[userid]
    # pick random brands that user has to buy from
    if not user.brand_list:
      num_brands_user = random.randint(1, num_brands/4+1)
      brands_list_copy = brands_list[:]
      for j in range(num_brands_user):
        index = random.randint(0, num_brands-j-1)
        user.brand_list[brands_list_copy[index]] = 1
        brands_list_copy.pop(index)
    # find possible nodes that user might buy (conditions on brand, size, not already purchased)
    possible_nodes = []
    for node in nodes_list:
      if abs(node.get_size() - user.get_true_size()) <= 20 and node not in user.node_rating_dict and node.brand in user.brand_list and not is_same_as_already_purchased_item(user, node):
        possible_nodes.append(node)
    if possible_nodes:
      # pick a random node to buy from that user is allowed to buy 
      nodeid = random.randint(0, len(possible_nodes)-1)
      node = possible_nodes[nodeid]
      rating = (node.get_size() - user.get_true_size() + 50) + random.randrange(-5,5)
      events.rate_event(user, node, rating)
      i += 1
    



initialize_brands()
initialize_users()
initialize_items()
make_purchases(num_purchases)

# dump graph (should only be used for small enough graphs (around 50*50 nodes))
# for node1 in graph.edge_matrix:
#   for node2 in graph.edge_matrix:
#     if node2 in graph.edge_matrix[node1]:
#       print (graph.edge_matrix[node1][node2].num_ratings),
#     else:
#       print("0"),
#   print("\n"),

# pick a random user and a random node of an item that user hasn't purchased (all sizes of it)
#   and run all algorithms on it (results get printed)
userid = random.randint(0, num_users-1)
user = users_list[userid]
nodeid = random.randint(0, num_items*nodes_per_item-1)
node = nodes_list[nodeid]
while node in user.node_rating_dict or is_same_as_already_purchased_item(user, node):
  nodeid = random.randint(0, num_items*nodes_per_item-1)
  node = nodes_list[nodeid]
events.ask_for_prediction("dijkstra", user, node)
events.ask_for_prediction("astar", user, node)
events.ask_for_prediction("kdirectional", user, node)
events.ask_for_prediction("perimeter_search", user, node, -math.log(0.3))
events.ask_for_prediction("beam_search", user, node)
