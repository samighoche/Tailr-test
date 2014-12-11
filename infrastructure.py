import math



class Node(object):
    def __init__(self, size, current_item_id, brand):
        self.id = current_item_id
        self.size = size
        self.brand = brand

    def get_id(self):
        return self.id

    def get_size(self):
        return self.size

    def get_brand(self):
        return self.brand

class Edge(object):
    def __init__(self, u, v, same_item = False):
        self.source = u
        self.end = v  
        self.mean_of_diffs = None
        self.list_of_diffs = None
        self.stdev = None
        self.num_ratings = None
        self.confidence = None
        self.cost = None
        self.same_item = same_item
        if same_item:
            self.confidence = 0.95
            self.cost = -math.log(self.confidence)
            self.mean_of_diffs = v.size - u.size

    def update_conf(self):
        self.confidence = max(min(.50*math.sqrt(self.num_ratings), 0.999999) - (self.stdev/3.0)*0.01, 0.01)
        # self.confidence = max(min(.50*self.num_ratings, 0.999999) - (self.stdev/3.0)*0.01, 0.01)
        self.cost = -math.log(self.confidence)


    def __repr__(self):
        return "%s->%s:\nmean_of_diffs:%s\nconfidence:%s\nsame_item:%s\nstdev:%s\nnum_ratings:%s\nlist_of_diffs:%s\n" % (self.source, self.end, self.mean_of_diffs, self.confidence, self.same_item, self.stdev, self.num_ratings, self.list_of_diffs)
 
class Graph(object):
    def __init__(self):
        self.edge_lst = {}
        self.neighbors_lst = {}
        self.edge_matrix = {}
        self.brand_matrix = {}

    def is_new_item(self, node):
        return not (node in neighbors_lst)
 
    def add_node(self, node):
        self.edge_lst[node] = []
        self.neighbors_lst[node] = []
        self.edge_matrix[node] = {}
        
 
    def get_edges(self, v):
        return self.edge_lst[v]

    def get_neighbors(self, v):
        return self.neighbors_lst[v]

    def get_edge_matrix(self):
        return self.edge_matrix

    def is_new_edge(self, u, v):
        return not (v in self.edge_matrix[u])
 
    def add_edge(self, u, v, same_item = False):
        # STILL NEED TO CHECK IF SAME ITEM IS TRUE AND PUT AN ARBITRARY DIFF OF RATINGS AND CONFIDENCE AND cost
        if u == v:
            raise ValueError("u == v")
        edge = Edge(u,v, same_item)
        reverse_edge = Edge(v,u, same_item)
        edge.reverse_edge = reverse_edge
        reverse_edge.reverse_edge = edge
        self.edge_lst[u].append(edge)
        self.edge_lst[v].append(reverse_edge)
        self.neighbors_lst[u].append(v)
        self.neighbors_lst[v].append(u)
        self.edge_matrix[u][v] = edge
        self.edge_matrix[v][u] = reverse_edge
        # print(u.brand)
        if u.brand is not None and v.brand not in self.brand_matrix[u.brand]:
            self.brand_matrix[u.brand][v.brand] = 1
            self.brand_matrix[v.brand][u.brand] = 1
        elif u.brand is not None:
            self.brand_matrix[u.brand][v.brand] += 1
            self.brand_matrix[v.brand][u.brand] += 1

    def update_edge(self, u, v, diff):
        edge = self.edge_matrix[u][v]
        num_ratings = edge.num_ratings
        if num_ratings == None:
            edge.mean_of_diffs = diff
            edge.stdev = 0
            edge.num_ratings = 1
            edge.list_of_diffs = [diff]
            edge.confidence = 0.55
            edge.cost = -math.log(edge.confidence)
        else:
            mean = edge.mean_of_diffs
            stdev = edge.stdev
            new_mean = (mean*num_ratings + diff)/(num_ratings+1)
            difference = (new_mean - mean)*(new_mean - mean)*num_ratings+(diff-new_mean)*(diff-new_mean)
            new_stdev = math.sqrt((stdev * stdev * num_ratings + difference)/(num_ratings+1))
            edge.mean_of_diffs = new_mean
            edge.stdev = new_stdev
            edge.num_ratings += 1
            edge.list_of_diffs.append(diff)
            edge.update_conf()

class User(object):
    def __init__(self, true_size, current_user_id, name=None):
        self.node_rating_dict = {}
        self.id = current_user_id
        self.true_size = true_size
        self.name = name
        self.brand_list = {}

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_true_size(self):
        return self.true_size

    def get_node_rating(self, node):
        return self.node_rating_dict[node]

    def rate_node(self, node, rating):

        self.node_rating_dict[node] = rating
        self.brand_list[node.brand] = 1



 