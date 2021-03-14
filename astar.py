

#import heapq
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



# number of expanded nodes and moves
nodes_expanded = 0
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
    'Pretty prints' the matrix.
    
    Arguments: 
        4 by 4 matrix (list of 4 lists with length 4)
"""       
def print_matrix(matrix):
  for i in range(len(matrix)):
    print(matrix[i])
  #print("\n")



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
    sys.exit('Too many or too few numbers entered')
    
  for i in range(len(arr)):
    if (arr[i] < 0 or arr[i] > 15):
      sys.exit('Input is of incorrect format.')

  return True



"""
    Node class for states of puzzle
    s
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
    self.g_n = None # distance from parent node
    self.h_n = None # cost to goal state
    self.f_n = None

        

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

  node = Node(new_matrix)
    
  node.parent = parent_node
  node.move = 'D'
    
  return node


"""
  Function for calculating heuristic 1 (misplaced_tiles)
"""
def h1_misplaced_tiles(matrix):
  misplaced_tiles = 0
  i, j = 0, 0
  while (i < 4):
    j = 0
    while (j < 4):
      # blank tile does not count in distance
      if (matrix[i][j] != goal_matrix[i][j] and matrix[i][j] != 0):
        misplaced_tiles = misplaced_tiles + 1 
      j = j + 1
    i = i + 1

  return misplaced_tiles


"""
  Function for calculating heuristic 2 (manhattan distance)
"""
def h2_manhattan_distance(matrix):
  i = 0
  distance = 0
  while (i < 4):
    j = 0
    while (j < 4):
      if(matrix[i][j] != goal_matrix[i][j] and matrix[i][j] != 0):
        value = matrix[i][j]
        k = 0
        while (k < 4):
          l = 0
          while (l < 4):
            if (goal_matrix[k][l] == value):
              dis = abs((i + j) - (k + l))
              distance = distance + dis
              l, k = 4, 4
            l = l + 1
          k = k + 1
      j = j + 1
    i = i + 1
  return distance



"""
    Function to solve 15 puzzle using a*.
    
    Arguments:
        4 by 4 matrix
        heuristic type
          'h1' or 'h2'
    Returns:
        goal state node (unless program exits due to an empty open list)
"""
def a_star(matrix, heuristic_type): 
  # head node
  initial_node = Node(matrix) 
  
  initial_node.g_n = 0
  initial_node.f_n = 0
  open = []
  closed = []

  open.append(initial_node)

  time1 = time.process_time()
  timed_out = time.process_time() - time1
  while (len(open) > 0):
    timed_out = time.process_time() - time1
    if (timed_out > 4):
      sys.exit('A* timed out')

    pop_index = 0
    
    i = 0
    # get index of the node with the lowest f(n)
    while (i < len(open)):
      if (open[i].f_n < open[pop_index].f_n):
        pop_index = i
      i += 1

    # pop node with the lowest f(n)
    node = open.pop(pop_index)
    if(node.matrix == goal_matrix):
      return node

    global nodes_expanded
    nodes_expanded += 1

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

    for child in children:
      if (child.matrix != None):

        # calculate f(n)
        child.g_n = node.g_n + 1
        child.h_n = None
        if (heuristic_type == 'h1'):
          child.h_n = h1_misplaced_tiles(child.matrix)
        else:
          child.h_n = h2_manhattan_distance(child.matrix)

        # calculate and save f(n) aka priority
        child.f_n = child.g_n + child.h_n

        # child already visited
        for n in closed:
          if (child == n):
            continue

        # child is already in open with lower g(n)
        for n in open:
          if (child.matrix == n.matrix and child.f_n > n.f_n):
            continue

        open.append(child)
        
    closed.append(node)

  # open is empty, no solution found
  sys.exit('A* failed to find a solution.')
    



        
        
       
def main():
  print('\n15 Puzzle using A*\n')

  input = get_user_input()    
  matrix = get_matrix(input)
    
  global nodes_expanded
  global moves
  
  #################################
  ##          run A*(h1)         ##
  #################################

  # start time and memory calculation right before call to bfs 
  process = psutil.Process(os.getpid())
  initial_memory = process.memory_info().rss / 1024.000000
  
  t = time.process_time()
  node = a_star(matrix, 'h1')

  # stop time and memory after bfs returns
  elapsed_time = time.process_time() - t
  final_memory = process.memory_info().rss / 1024.000000
    
    
  # loop returned bfs node, and get moves
  while (node is not None):
    if (node.parent == None):
      break
    moves.insert(0, node.move)
    node = node.parent
  
  print("--------------------------------------------------")
  # print moves, nodes expanded, time, and memory usage for A*(h1)
  print('\n15 Puzzle using A* (using h1)')
  print('Moves: ', moves)
  print('Number of Nodes  Expanded: ', nodes_expanded)
  print("Time Taken: ", '%.5f' % elapsed_time)
  print('Memory Used: ', '{0:.6f} KB'.format(final_memory - initial_memory))



  #################################
  ## do the same thing for A*(h2)##
  #################################
  nodes_expanded = 0
  moves = []

  initial_memory = process.memory_info().rss / 1024.000000
  t = time.process_time()
  node = a_star(matrix, 'h2')

  elapsed_time = time.process_time() - t
  final_memory2 = process.memory_info().rss / 1024.000000
    
  while (node is not None):
    if (node.parent == None):
      break
    moves.insert(0, node.move)
    node = node.parent

  print('\n15 Puzzle using A* (using h2)')
  print('Moves: ', moves)
  print('Number of Nodes  Expanded: ', nodes_expanded)
  print("Time Taken: ", '%.5f' % elapsed_time)
  print('Memory Used: ', '{0:.6f} KB'.format(final_memory2 - final_memory))
    


if __name__ == '__main__':
  main()    
    
    
    
    
    
    
    
    
    
    
    
    
    
