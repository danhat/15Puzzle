
from queue import Queue
import time
import os
import psutil
import sys
import copy




"""
  goal state matrix, used to check if goal state is reached
"""
goal_matrix = [
  [1, 2, 3, 4],
  [5, 6, 7, 8],
  [9, 10, 11, 12],
  [13, 14, 15, 0]
]




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
    self.g_n = None # distance from parent node
    self.h_n = None # cost to goal state
    self.f_n = None # g_n + f_n




"""
  Get the children nodes (nodes derived from going right, left, down, and up) of the current node

  Arguments:
    node (Node): node to get the children of
    expanded (list): list of nodes already visited

  Returns:
    children (list of <Node>): children nodes
"""
def get_children(node, expanded): 
  # get position of blank tile
  x, y, i, j = 99, 99, 0, 0
  while (i < 4):
    j = 0
    while (j < 4):
      if (node.matrix[i][j] == 0):
        x, y = i, j
      j = j + 1
    i = i + 1
    
  moves = [(x, y + 1, 'R'), (x, y - 1, 'L'), (x - 1, y, 'U'), (x + 1, y, 'D')]
  children = []
  
  for move in moves:
    # check boundaries
    curr_x = move[0]
    curr_y = move[1]
    move_name = move[2]
    
    if (curr_y > 3 or curr_y < 0 or curr_x > 3 or curr_x < 0):
      children.append(Node())
      continue
    
    # deep copy of argument matrix
    new_matrix = copy.deepcopy(node.matrix)
    # perform swap
    swap_num = new_matrix[curr_x][curr_y] 
    new_matrix[x][y] = swap_num
    new_matrix[curr_x][curr_y] = 0
    
    
    # if node has already been expanded, dont create new node
    if(expanded.__contains__(new_matrix)):
      children.append(Node())
      continue
      
    
    # node hasnt been expanded, so create a new node to be added to queue
    child = Node(new_matrix) 

    # set node's parent and move
    child.parent = node
    child.move = move_name

    children.append(child)  

    
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
  Prints the moves, number of nodes expanded, time taken, and the memory used to find the solution
"""
def print_search_info(node, expanded_nodes_count, elapsed_time, memory_used):
  moves = []
  
  while (node is not None):
    if (node.parent == None):
      break
    moves.insert(0, node.move)
    node = node.parent

  # print moves, nodes expanded, time, and memory usage
  print('Moves: ', moves)
  print('Number of Nodes  Expanded: ', expanded_nodes_count)
  print("Time Taken: ", '%.7f' % elapsed_time, 'seconds')
  print('Memory Used: ', '{0:.3f} KB'.format(memory_used) + '\n')

