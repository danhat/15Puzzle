"""
Danielle Hatten
15 Puzzle Using Breadth First Search
February 2020
"""


from queue import Queue
import time
import os
import psutil
import sys
import copy



# goal state matrix, used to check if goal state is reached
goal_matrix = [
  [1, 2, 3, 4],
  [5, 6, 7, 8],
  [9, 10, 11, 12],
  [13, 14, 15, 0]
]

# list for expanded nodes and list for moves
expanded = []
moves = []



"""
  Gets keyboard input for input file name, parses input file,
  and returns a list of integers.
    
  Returns:
    list of integers
"""
def get_user_input():
  # get keyboard input
  filename = input('Enter the file name to read from: ')
  filename = 'input/' + filename
    
  # open and parse file, store integers in a list
  f = open(filename, 'r') 
  line = f.readline()
  results = line.split(', ')
  results = [int(i) for i in results]
    
  f.close()
  return results
  
 

    
"""
  Converts input list of integers into a matrix and returns
  the matrix.
    
  Arguments:
    arr: list of integers
        
  Returns:
    4 by 4 matrix (list of 4 lists with length 4)
"""
def get_matrix(arr):
    
  check_input(arr)
        
    
  matrix = [
    [arr[0], arr[1], arr[2], arr[3]],
    [arr[4], arr[5], arr[6], arr[7]],
    [arr[8], arr[9], arr[10], arr[11]],
    [arr[12], arr[13], arr[14], arr[15]]
  ]

  return matrix


"""
  Checks that input list is the correct lengeth (16) and 
  checks that input integers are in the correct range.
  Program exits if error is found.
    
  Arguments:
    arr: list of integers
    
  Returns:
    True (unless program exits due to error)
"""
def check_input(arr):
  if(len(arr) != 16):
    sys.exit('Input Error: Too many or too few numbers entered')
    
  for i in range(len(arr)):
    if (arr[i] < 0 or arr[i] > 15):
      sys.exit('Input Error: Input is of incorrect format.')

    j = i + 1
    while (j < 16):
      if (arr[i] == arr[j]):
        sys.exit('Input Error: Input contains a repeated number')
      j = j + 1
    
  return True

 
    
"""
  'Pretty prints' the matrix.
    
  Arguments: 
    4 by 4 matrix (list of 4 lists with length 4)
"""       
def print_matrix(matrix):
  for i in range(len(matrix)):
    print(matrix[i])
  #print("\n")




"""
  Node class for states of puzzle
    
  Contents:
    matrix: state of puzzle
    parent: state of puzzle that the node is derived from
    move: move made by parent node to get to state
"""
class Node:
  def __init__(self, dataval = None):
    self.matrix = dataval
    self.parent = None
    self.move = None




"""
  New puzzle state created by moving the blank tile to the right.
    
  Arguments:
    matrix: 4 by 4 matrix to be changed
    x: x positon of blank tile
    y: y position of blank tile
    parent_node: matrix that the new state is to be derived from
  Returns:
    newly created node formed by moving blank tile to the right
    or uninitialized node.
"""
def move_right(matrix, x, y, parent_node):
        
  # if blank tile is on the border, nothing to change or add
  if (y + 1 > 3):
    return Node()
    
  # deep copy of argument matrix
  new_matrix = copy.deepcopy(matrix)
  # perform swap
  swap = new_matrix[x][y + 1] 
  new_matrix[x][y] = swap
  new_matrix[x][y + 1] = 0
    
  # if node has already been expanded, dont create new node
  if(expanded.__contains__(new_matrix)):
    return Node()
    
  # node hasnt been expanded, so create a new node to be added to queue
  node = Node(new_matrix) 
    
  # set node's parent and move
  node.parent = parent_node
  node.move = 'R'
    
  return node



"""
  New puzzle state created by moving the blank tile to the left.
    
  Arguments:
    matrix: 4 by 4 matrix to be changed
    x: x positon of blank tile
    y: y position of blank tile
    parent_node: matrix that the new state is to be derived from
  Returns:
    newly created node formed by moving blank tile to the left
    or uninitialized node.
"""    
def move_left(matrix, x, y, parent_node):
    
  if (y - 1 < 0):
    return Node()
    
  new_matrix = copy.deepcopy(matrix)
  swap = new_matrix[x][y - 1]
  new_matrix[x][y] = swap
  new_matrix[x][y - 1] = 0
    
  if(expanded.__contains__(new_matrix)):
    return Node()
    
    
  node = Node(new_matrix) 
    
  node.parent = parent_node
  node.move = 'L'
    
  return node




"""
  New puzzle state created by moving the blank tile up.
    
  Arguments:
    matrix: 4 by 4 matrix to be changed
    x: x positon of blank tile
    y: y position of blank tile
    parent_node: matrix that the new state is to be derived from
  Returns:
    newly created node formed by moving blank tile up
    or uninitialized node.
"""
def move_up(matrix, x, y, parent_node):
    
  if (x - 1 < 0):
    return Node()
    
  new_matrix = copy.deepcopy(matrix)
  swap = new_matrix[x - 1][y]
  new_matrix[x][y] = swap
  new_matrix[x - 1][y] = 0
    
  if(expanded.__contains__(new_matrix)):
    return Node()
    
  node = Node(new_matrix)
    
  node.parent = parent_node
  node.move = 'U'
    
  return node




"""
  New puzzle state created by moving the blank tile down.
    
  Arguments:
    matrix: 4 by 4 matrix to be changed
    x: x positon of blank tile
    y: y position of blank tile
    parent_node: matrix that the new state is to be derived from
  Returns:
    newly created node formed by moving blank tile down
    or uninitialized node.
"""
def move_down(matrix, x, y, parent_node):
   
  if (x + 1 > 3):
    return Node()
        
    
  new_matrix = copy.deepcopy(matrix)   
  swap = new_matrix[x + 1][y]
  new_matrix[x][y] = swap
  new_matrix[x + 1][y] = 0
    
  if(expanded.__contains__(new_matrix)):
    return Node()
    
  node = Node(new_matrix)
    
  node.parent = parent_node
  node.move = 'D'
    
  return node





"""

"""
def get_children(node): 
  # get position of blank tile
  x, y, i, j = 99, 99, 0, 0
  while (i < 4):
    j = 0
    while (j < 4):
      if (node.matrix[i][j] == 0):
        x, y = i, j
      j = j + 1
    i = i + 1

  # get children
  right_child = move_right(node.matrix, x, y, node)
  left_child = move_left(node.matrix, x, y, node)
  up_child = move_up(node.matrix, x, y, node)
  down_child = move_down(node.matrix, x, y, node)

  children = [right_child, left_child, up_child, down_child]

  return children




"""
  Function to solve 15 puzzle using bfs.
    
  Arguments:
    4 by 4 matrix
  Returns:
    goal state node (unless program exits due to an empty queue)
"""
def bfs(matrix): 
  # head node
  initial_node = Node(matrix) 

  # check to see if initial matrix is the goal state
  # if so, return that node
  if (initial_node.matrix == goal_matrix):
    return initial_node
    
  # initialize queue and enqueue head node
  q = Queue()
  q.put(initial_node)  

  while True:
    # if queue is empty, no solution is able to be found using this program
    if(q.empty() == True):
      sys.exit('BFS failed to find a solution.')
        
    # get node at the front of queue
    node = q.get()
        
    # if node has not been expanded yet, add it to expanded nodes
    if (expanded.__contains__(node.matrix) == False):
      expanded.append(node.matrix)
        
    children = get_children(node)

    for child in children:
      if (child.matrix == goal_matrix):
        return child
      if (child.matrix != None):
        q.put(child)
        
    
        
    
    
def main():
  print('\n**15 Puzzle using BFS**\n')

  input = get_user_input()    
  matrix = get_matrix(input)
    
    
  print('\ninitial state:')
  print_matrix(matrix)
    
  # start time right before call to bfs  
  t = time.process_time()
  node = bfs(matrix)

  # stop time after bfs returns
  elapsed_time = time.process_time() - t
    
  # get memory usage
  process = psutil.Process(os.getpid())
    
  print('\ngoal state:')
  print_matrix(node.matrix)
    
  # loop returned bfs node, and get moves
  while (node is not None):
    if (node.parent == None):
      break
    moves.insert(0, node.move)
    node = node.parent
     
  # print moves, nodes expanded, time, and memory usage
  print('\nMoves: ', moves)
  print('Number of Nodes  Expanded: ', len(expanded))
  print("Time Taken: ", '%.5f' % elapsed_time, 'nanoseconds')
  print('Memory Used: ', '{0:.2f} KB'.format((process.memory_info().rss)/1024))
    


if __name__ == '__main__':
  main()    
    
    
    
    
    
    
    
    
    
    
    
    
    
