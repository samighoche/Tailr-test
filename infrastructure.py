import math
import global_vars

class Node(object):
    def __init__(self, size, brand=None, name=None):
        global current_item_id
        global graph
        self.id = current_item_id
        current_item_id += 1
        self.size = size
        self.brand = brand
        self.name = name
        graph.add_node(self)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_size(self):
        return self.size

    def get_brand(self):
        return self.brand

class Edge(object):
    def __init__(self, u, v, same_item = False):
        self.source = u
        self.end = v  
        self.mean_of_diffs = None
        self.stdev = None
        self.num_ratings = None
        self.conf = None
        self.same_item = same_item

    def update_conf(self):
        raise ValueError("Not implemented yet")


    def __repr__(self):
        return "%s->%s:\ndiff:%s\nconf:%ssame_item:%s" % (self.source, self.sink, self.mean_of_diffs, self.conf, self.same_item)
 
class Graph(object):
    def __init__(self):
        self.edge_lst = {}
        self.neighbors_lst = {}
        self.edge_matrix = {}

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
        return not (edge in self.edge_matrix[u][v])
 
    def add_edge(self, u, v, same_item = False):
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

    def update_edge(self, u, v, diff):
        edge = self.edge_matrix[u][v]
        num_ratings = edge.num_ratings
        if self.num_ratings == None:
            edge.mean_of_diffs = diff
            edge.stdev = 0
            edge.num_ratings = 1
            edge.update_conf()
        else:
            mean = edge.mean_of_diffs
            stdev = edge.stdev
            new_mean = (mean*num_ratings + diff)/(num_ratings+1)
            difference = (new_mean - mean)*(new_mean - mean)*num_ratings+(diff-new_mean)*(diff-new_mean)
            new_stdev = math.sqrt((stdev * stdev * num_ratings + difference)/(num_ratings+1))
            edge.mean_of_diffs = new_mean
            edge.stdev = new_stdev
            edge.num_ratings += 1
            edge.update_conf()

class User(object):
    def __init__(self, true_size, name=None):
        self.node_rating_dict = {}
        global current_user_id
        self.id = current_user_id
        current_user_id += 1
        self.true_size = true_size
        self.name = name

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


 