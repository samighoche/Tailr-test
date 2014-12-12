import heapq

# Priority queue that uses heapq
class PriorityQueue:
  def __init__(self):
    self.heap = []
    self.set = {}
  
  # push node on heap   
  def push(self, node, value):
    # if already in heap, update value
    if node in self.set:
      self.set[node][0] = value
      heapq.heapify(self.heap)
    # if not in heap, add to heap
    else:
      heapq.heappush(self.heap, [value, node])
      self.set[node] = [value, node]

  # extract min
  def pop(self):
    if not self.heap:
        return None
    node = heapq.heappop(self.heap)[1]
    del self.set[node]
    return node

  # return priority of node in heap
  def getPriority(self, node):
    if node in self.set:
      return self.set[node][0]
    return None

  # return whether queue is empty
  def is_empty(self):
    return not self.heap