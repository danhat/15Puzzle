

from helperfunctions import *



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
def dls(node, depth, expanded_nodes):
  # goal node is found, return it
  if (node.matrix == goal_matrix):
    return node, True, expanded_nodes

  # depth limit reached, so return None, True 
  # bc there may be children node to search
  elif (depth == 0):
    return Node(), True, expanded_nodes
  
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
    children = get_children(node, expanded_nodes)

    for child in children:
      # check if child exists
      if (child.matrix != None):
        # add to expanded
        expanded_nodes.append(child.matrix)
        # call dls for child if it exists
        found, remaining, expanded_nodes = dls(child, depth - 1, expanded_nodes)
        if (found.matrix != None):
          # goal node found, return it
          return found, True, expanded_nodes
        # goal node not found, but there are remaining nodes
        if (remaining == True):
          nodes_remaining = True
    
    # no remaining nodes => end iddfs
    return Node(), nodes_remaining, expanded_nodes




    
"""
  Iterative Deepening Depth First Search function.
  Searches for goal node by increasing the depth limit by 1 with each iteration.
    
  Arguments:
    node: Node object containing the initial state
        
  Returns:
    an unitialized node if goal is not found or the goal node if the goal node is reached      
        
"""
def iddfs(matrix, return_info):
  # start time right before call to bfs  
  initial_time = time.process_time()

  # start memory usage calculation
  process = psutil.Process(os.getpid())
  initial_memory = process.memory_info().rss / 1024.000000

  expanded_nodes_count = 0
  expanded_nodes = []
  
  node = Node(matrix)
  
  # begin at depth 0
  depth = 0

  while (depth >= 0):
    timed_out = time.process_time() - initial_time
    if (timed_out > 3):
      print('\n**IDDFS timed out**')
      return

    expanded_nodes_count = expanded_nodes_count + len(expanded_nodes)

    # reset visited list for next iteration of dls
    expanded_nodes = []
    expanded_nodes.append(node.matrix)
    found, remaining, expanded_nodes = dls(node, depth, expanded_nodes)

    if (found.matrix != None):
      # stop time when goal matrix is found
      elapsed_time = time.process_time() - initial_time
      # get memory usage
      final_memory = process.memory_info().rss / 1024.000000
      memory_used = final_memory - initial_memory
      if (return_info == True):
        return (found, expanded_nodes_count, elapsed_time, memory_used)
      else:
        print_search_info(found, expanded_nodes_count, elapsed_time, memory_used)
      return found
    # dls will set remaining to false when there are no more nodes to expand
    # function will then stop looping and return an empty node
    elif(remaining == False):
      return Node()
    depth = depth + 1

    
    
def main():

  input = get_user_input()    
  matrix = get_matrix(input)  
  
  print('\n15 Puzzle using IDDFS')

  print('\nInitial State: \n')
  print_matrix(matrix)
  print('\n')

  node = iddfs(matrix, False)
    


if __name__ == '__main__':
  main()    