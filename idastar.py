"""
Danielle Hatten
15 Puzzle Using Iterative Deepening A*
March 2020
"""


import time
import os
import psutil
import sys
import copy

nodes_expanded = 0
explored = []
heuristic = 'h1'


# goal state matrix, used to check if goal state is reached
goal_matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]



"""
  Function to get which heuristic the user wants to use:
    h1 for misplaced tiles,
    h2 for manhattan distance
"""
def get_heuristic():
  global heuristic
  h = '0'
  valid_heuristics = ['h1', 'h2']

  while (h not in valid_heuristics):
    if (h == 'q'):
      sys.exit()
    h = input('\n > Enter a heuristic to use (h1 for misplaced tiles or h2 for manhattan distance): ')

  return h
  


"""
  Gets keyboard input for input file name, parses input file,
  and returns a list of integers.
    
  Returns:
    list of integers
"""
def get_user_input():
  # get keyboard input
  filename = input('\n > Enter the file name to read from (or \'q\' to quit): ')

  if (filename == 'q'):
    sys.exit()

  global heuristic
  if (filename == 'h'):
      heuristic = get_heuristic()
      filename = input('\n > Enter the file name to read from (or \'q\' to quit): ')

  filename = 'input/' + filename
    
  # open and parse file, store integers in a list
  f = open(filename, 'r') 
  line = f.readline()
  results = line.split(', ')
  results = [int(i) for i in results]
    
  f.close()
  return results
  



def get_keyboard_input():
  input_correct = False, []
  while (input_correct[0] == False):
    user_input = input('\n > Enter the numbers with each number separated by a comma (or \'q\' to quit): ')

    if (user_input == 'q'):
      sys.exit()

    global heuristic
    if (user_input == 'h1'):
      heuristic = 'h1'
      print('Heuristic is now set to h1')
      user_input = input('\n > Enter the numbers with each number separated by a comma (or \'q\' to quit): ')
    elif (user_input == 'h2'):
      heuristic = 'h2'
      print('Heuristic is now set to h2')
      user_input = input('\n > Enter the numbers with each number separated by a comma (or \'q\' to quit): ')

    input_correct = check_keyboard_input(user_input)

  return input_correct[1]
  

def check_keyboard_arr(arr):
  try:
    arr = arr.split(',')
  except: 
    print('Input Error: Numbers are not sepated by a comma')
    return False, []
  
  try:
    arr = [int(numeric_string) for numeric_string in arr]
  except:
    print('Input Error: Non-intergers entered')
    return False, []

  if(len(arr) != 16):
    print('Input Error: Too many or too few numbers entered')
    return False, []
    
  for i in range(len(arr)):
    if (arr[i] < 0 or arr[i] > 15):
      print('Input Error: Input is of incorrect format.')
      return False, []

    j = i + 1
    while (j < 16):
      if (arr[i] == arr[j]):
        print('Input Error: Input contains a repeated number')
        return False, []
      j = j + 1
    
  return True, arr





    
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
    Node class for states of puzzle.
    
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
  Function to get children of given node.
  Argument:
    node to get children of
  Returns:
    list of children
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
              #dis = abs((i + j) - (k + l))
              dis = abs(i - k) + abs(j - l)
              distance = distance + dis
              l, k = 4, 4
            l = l + 1
          k = k + 1
      j = j + 1
    i = i + 1
  return distance




"""
  Helper function to idastar().
  Arguments:
    path: nodes being searched
    g: step cost
    cutoff: current threshold
  Returns:
    'found' if solution is found
    new cutoff(int) if higher cutoff is needed
    float('inf') if no solution
"""
def search(path, g, cutoff): 
  node = path[0]
  
  global heuristic
  global explored
  global nodes_expanded

  explored.append(node.matrix)
  nodes_expanded += 1


  #if (nodes_expanded % 10000 == 0):
    #print(nodes_expanded)

  f_n = 0 
  if (heuristic == 'h1'):
    f_n = g + h1_misplaced_tiles(node.matrix)
  else:
    f_n = g + h2_manhattan_distance(node.matrix)

  if (f_n > cutoff):
    #print('cutoff reached')
    return f_n  # greater f found

  if (node.matrix == goal_matrix):
    return 'found' 

  min = float('inf')

  for child in get_children(node):
    # node already explored or in path, so skip it
    if child.matrix in explored:
      continue
    if child in path:
      continue

    # if child is not None, search recursively
    if (child.matrix != None):
      path.insert(0, child)        
      temp = search(path, g + 1, cutoff)

      if (temp == 'found'):
        # solution found
        return 'found'

      if (temp < float('inf')):
        # higher cutoff found
        min = temp

      path.pop(0)

  # no solution, return infinity
  return min




"""
  Function to solve 15 puzzle with Iterative Deepening A*
  Arguments:
    matrix: 4 by 4, list of 4 lists
"""
def idastar(matrix):
  global heuristic
  global nodes_expanded
  global explored

  # initialization
  path = []
  nodes_expanded = 0
  cutoff = 0

  # set cutoff
  if (heuristic == 'h1'):
    cutoff = h1_misplaced_tiles(matrix)
  else:
    cutoff = h2_manhattan_distance(matrix)

  root = Node(matrix)
  path.insert(0, root)

  iterations = 0

  while True:
    explored = []

    iterations += 1

    # begin searching
    temp = search(path, 0, cutoff)

    if (temp == 'found'):
      print('\nSolved in', iterations, 'iterations using', heuristic)
      return path[0]

    # no solution
    if (temp == float('inf')):
      sys.exit('This algorithm was not able to find a solution')

    # increase cutoff
    cutoff = temp
    




       
def main():
  process = psutil.Process(os.getpid())
  initial_memory = process.memory_info().rss / 1024.000000
  print('------------------------------------------')
  print('| 15 Puzzle using Iterative Deepening A* |')
  print('------------------------------------------')

  print('\nEnter \'h\' any time to swich heuristics.')

  global heuristic
  heuristic = get_heuristic()

  input = get_user_input()
  final_memory = 0
  
  while (input != 'q'):
    if (input == 'h'):
      heuristic = get_heuristic()
    matrix = get_matrix(input)
  
    global nodes_expanded
    global moves
 
    # start time and memory calculation right before call to idastar 
    t = time.process_time()
  
    node = idastar(matrix)

    # stop time and memory after idastar returns
    elapsed_time = time.process_time() - t
    final_memory = process.memory_info().rss / 1024.000000
    
    moves = []
    # loop returned idastar node, and get moves
    while (node is not None):
      if (node.parent == None):
        break
      moves.insert(0, node.move)
      node = node.parent
  
    
    # print moves, nodes expanded, time, and memory usage for idastar
    print('\nMoves: ', moves)
    print('Number of Nodes  Expanded: ', nodes_expanded)
    print('Time Taken: ', '%.5f' % elapsed_time)
    print('Memory Used: ', '{0:.6f} KB'.format(final_memory - initial_memory))
    print('----------------------------------------------------')
    input = get_user_input()
  





if __name__ == '__main__':
  main()    
    
    
    
     
