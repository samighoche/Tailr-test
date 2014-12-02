import heapq

# Priority queue that uses heapq
class PriorityQueue:
  def __init__(self):
    self.heap = []
    self.set = {}
      
  def push(self, node, value):
    if node in self.set:
      self.set[node][0] = value
      heapq.heapify(self.heap)
    else:
      heapq.heappush(self.heap, [value, node])
      self.set[node] = [value, node]

  def pop(self):
    if not self.heap:
        return None
    node = heapq.heappop(self.heap)[1]
    del self.set[node]
    return node

  def getPriority(self, node):
    if node in self.set:
      return self.set[node][0]
    return None