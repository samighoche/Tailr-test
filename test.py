import global_vars
import infrastructure
import random
import events
import time

# Someone please replace these lines with sys args (the program should take these as arguments like in the psets)
num_users = int(raw_input("Please enter the number of users for this trial"))
num_items = int(raw_input("Please enter the number of items for this trial (there will be 10 nodes for each item)"))
num_purchases = int(raw_input("Please enter the number of purchases for this trial"))


users_list = []
nodes_list = []
global graph

def initialize_users():
	for i in range(num_users):
	    true_size = random.randint(20,80)
	    user = infrastructure.User(true_size)
	    users_list.append(user)

def initialize_items():
  for i in range(num_items):
  	same_items = []
  	for j in range(10):
  		size = random.randint(20+j*10, 80)
  		node = infrastructure.Node(size)
  		for other_size in same_items:
  			graph.add_edge(node, other_size, True)
  		same_items.append(node)
  		nodes_list.append(node)

def make_purchases(num_purchases):
  for i in range(num_purchases):
    userid = random.randint(0, num_users-1)
    user = users_list[userid]
    nodeid = random.randint(0, num_items-1)
    node = nodes_list[nodeid]
    if node not in user.node_rating_dict:
    	while abs(node.get_size() - user.get_true_size()) > 20:
        	nodeid = random.randint(0,num_items-1)
        	node = nodes_list[nodeid]
      rating = (node.get_size() - user.get_true_size() + 50) + random.randrange(-5,5)
      events.rate_Event(user, node, rating)


initialize_users()
initialize_items()
make_purchases(num_purchases)
for user in users_list:
	count = 0
	total = 0
	for node in nodes_list:
		if node not in user.node_rating_dict:
			starttime = time.time()
			prediction = events.ask_for_prediction_dijkstra(user, node)
			duration = time.time() - starttime
			#compute accuracy
			total += duration
			count += 1
	print # some measure of accuracy plus average time for this person = total/count if count is not 0
# repeat for non-admissible heuristic approach and beam_search

