"""
Danielle Hatten
15 Puzzle Using Iterative Deepening Depth First Search (and Depth Limited Search as a Helper)
February 2020
"""

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
expanded_nodes = 0
moves = []
visited = []



"""
    Gets keyboard input for input file name, parses input file,
    and returns a list of integers.
    
    Returns:
        list of integers
"""
def get_user_input():
    # get keyboard input
    filename = input('Enter the file name to read from: ')
    
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
    if(visited.__contains__(new_matrix)):
        return Node()
    
    # node hasnt been visited, so create a new node and mark the matrix as visited
    visited.append(new_matrix)
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
    
    if(visited.__contains__(new_matrix)):
        return Node()
    
    visited.append(new_matrix)    
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
    
    if(visited.__contains__(new_matrix)):
        return Node()
    
    visited.append(new_matrix)
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
    
    if(visited.__contains__(new_matrix)):
        return Node()
    
    visited.append(new_matrix)
    node = Node(new_matrix)
    
    node.parent = parent_node
    node.move = 'D'
    
    return node






"""
    Recursive helper function to iddfs().
    Depth Limited Search function.
    Searches for goal node up until depth limit which is passed as an arg
    
    Arguments:
      node: Node object containing the matrix, move to get to the state, and the parent of the node
      depth: the depth to search to on a node
        
    Returns:
      (Node(), boolean)
      an unitialized node if goal is not found or the goal node
      True if there are children nodes, False if there are no children nodes      
        
"""
def dls(node, depth): 
  # goal node is found, return it
  if (node.matrix == goal_matrix):
    return node, True

  # depth limit reached, so return None, True 
  # bc there may be children node to search
  elif (depth == 0):
    return Node(), True
  
  # depth limit not reached and goal node not found,
  # so get children and continue dls
  else:
    # get position of blank tile
    x, y, i, j = 99, 99, 0, 0
    while (i < 4):
      j = 0
      while (j < 4):
        if (node.matrix[i][j] == 0):
          x, y = i, j
        j = j + 1
      i = i + 1
        
    nodes_remaining = False

    # get children 
    right_child = move_right(node.matrix, x, y, node)
    left_child = move_left(node.matrix, x, y, node)
    up_child = move_up(node.matrix, x, y, node)
    down_child = move_down(node.matrix, x, y, node)

    children = [right_child, left_child, up_child, down_child]

    for child in children:
      # check if child exists
      if (child.matrix != None):
        # call dls for child if it exists
        found, remaining = dls(child, depth - 1)
        if (found.matrix != None):
          # goal node found, return it
          return found, True
        # goal node not found, but there are remaining nodes
        if (remaining == True):
          nodes_remaining = True
    
    # no remaining nodes => ends iddfs
    return Node(), nodes_remaining


    
"""
    Iterative Deepening Depth First Search function.
    Searches for goal node by increasing the depth limit by 1 with each iteration.
    
    Arguments:
      node: Node object containing the initial state
        
    Returns:
      an unitialized node if goal is not found or the goal node if the goal node is reached      
        
"""
def iddfs(node):
  global expanded_nodes
  global visited
  
  # begin at depth 0
  depth = 0
  while (depth >= 0):
    expanded_nodes = expanded_nodes + len(visited)
    # reset visited list for next iteration of dls
    visited = []
    visited.append(node.matrix)
    found, remaining = dls(node, depth)
    if (found.matrix != None):
      return found
    # dls will set remaining to false when there are no more nodes to expand
    # function will then stop looping and return an empty node
    elif(remaining == False):
      return Node()
    depth = depth + 1

    
    
def main():
    print('\n**15 Puzzle using IDDFS**\n')

    input = get_user_input()    
    matrix = get_matrix(input)    
    
    print('\ninitial state:')
    print_matrix(matrix)
    
    # start time right before call to bfs  
    initial_time = time.process_time()

    # start memory usage calculation
    process = psutil.Process(os.getpid())

    # run iddfs
    root = Node(matrix)
    node = iddfs(root)

    # stop time after bfs returns
    elapsed_time = time.process_time() - initial_time

    if (node.matrix == None):
      sys.exit('IDDFS failed to find a solution.')
    
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
    print('Number of Nodes  Expanded: ', expanded_nodes)
    print("Time Taken: ", '%.5f' % elapsed_time)
    print('Memory Used: ', '{0:.2f} KB'.format((process.memory_info().rss)/1024))
    


if __name__ == '__main__':
    main()    