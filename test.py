from global_vars import current_user_id, current_item_id, graph
import infrastructure
import random
import events
import time

# Someone please replace these lines with sys args (the program should take these as arguments like in the psets)
# num_users = int(raw_input("Please enter the number of users for this trial"))
# num_items = int(raw_input("Please enter the number of items for this trial (there will be 10 nodes for each item)"))
# num_purchases = int(raw_input("Please enter the number of purchases for this trial"))
# num_brands = int(raw_input("Please enter the number of brands for this trial"))

num_users = 20
num_items = 50
num_purchases = 400
num_brands = 2
nodes_per_item = 1

users_list = [None for i in range(num_users)]
nodes_list = [None for i in range(num_items*nodes_per_item)]
brands_list = [None for i in range(num_brands)]
global graph

def initialize_users():
  for i in range(num_users):
    true_size = random.randint(30,70)
    global current_user_id
    user = infrastructure.User(true_size, current_user_id)
    current_user_id += 1
    users_list[i] = user

def initialize_items():
  for i in range(num_items):
    same_items = []
    for j in range(nodes_per_item):
      # GOTTA FIX THIS HERE
      size = random.randint(30+j*10, 70)
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
  
def initialize_brands():
  for i in range(num_brands):
    brands_list[i] = "brand" + str(i)

def is_same_as_already_purchased_item(user, node):
  for purchase in user.node_rating_dict:
    if node in graph.edge_matrix[purchase] and graph.edge_matrix[purchase][node].same_item:
      return True
  return False

def make_purchases(num_purchases):
  i = 0
  while i < num_purchases:
    userid = random.randint(0, num_users-1)
    user = users_list[userid]
    if not user.brand_list:
      num_brands_user = random.randint(1, num_brands)
      brands_list_copy = brands_list[:]
      for j in range(num_brands_user):
        index = random.randint(0, num_brands-j-1)
        user.brand_list[brands_list_copy[index]] = 1
        brands_list_copy.pop(index)
    possible_nodes = []
    for node in nodes_list:
      if abs(node.get_size() - user.get_true_size()) <= 20 and node not in user.node_rating_dict and node.brand in user.brand_list and not is_same_as_already_purchased_item(user, node):
        possible_nodes.append(node)
    if possible_nodes:
      nodeid = random.randint(0, len(possible_nodes)-1)
      node = possible_nodes[nodeid]
      rating = (node.get_size() - user.get_true_size() + 50) + random.randrange(-5,5)
      events.rate_event(user, node, rating)
    i += 1



initialize_brands()
initialize_users()
initialize_items()
make_purchases(num_purchases)

# for node1 in graph.edge_matrix:
#   for node2 in graph.edge_matrix:
#     if node2 in graph.edge_matrix[node1]:
#       print (graph.edge_matrix[node1][node2].num_ratings),
#     else:
#       print("0"),
#   print("\n"),


userid = random.randint(0, num_users-1)
user = users_list[userid]
nodeid = random.randint(0, num_items*nodes_per_item-1)
node = nodes_list[nodeid]

while node in user.node_rating_dict or is_same_as_already_purchased_item(user, node):
  nodeid = random.randint(0, num_items*nodes_per_item-1)
  node = nodes_list[nodeid]
events.ask_for_prediction_dijkstra(user, node)

for i in list(user.node_rating_dict.keys()):
  goal = i
  #goal = random.choice(list(user.node_rating_dict.keys()))
  events.ask_for_prediction_bidirectional(node, goal, user)
  
# for user in users_list:
# 	count = 0
# 	total = 0
# 	for node in nodes_list:
# 		if node not in user.node_rating_dict:
# 			starttime = time.time()
# 			prediction = events.ask_for_prediction_dijkstra(user, node)
# 			duration = time.time() - starttime
# 			#compute accuracy
# 			total += duration
# 			count += 1
# 	print # some measure of accuracy plus average time for this person = total/count if count is not 0
# repeat for non-admissible heuristic approach and beam_search

