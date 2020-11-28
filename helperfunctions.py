from queue import Queue
import time
import os
import psutil
import sys
import copy



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
    self.f_n = None


"""

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

"""
def print_search_info(node, expanded_nodes_count, elapsed_time, memory_used):
  moves = []
  
  while (node is not None):
    if (node.parent == None):
      break
    moves.insert(0, node.move)
    node = node.parent

  # print moves, nodes expanded, time, and memory usage
  print('\nMoves: ', moves)
  print('Number of Nodes  Expanded: ', expanded_nodes_count)
  print("Time Taken: ", '%.7f' % elapsed_time, 'nanoseconds')
  print('Memory Used: ', '{0:.2f} KB'.format(memory_used) + '\n')