

from helperfunctions import *






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
def search(path, g, cutoff, heuristic): 
  node = path[0]
  
  explored_nodes.append(node.matrix)

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

  for child in get_children(node, []):
    # node already explored or in path, so skip it
    if child.matrix in explored_nodes:
      continue
    if child in path:
      continue

    # if child is not None, search recursively
    if (child.matrix != None):
      path.insert(0, child)        
      temp = search(path, g + 1, cutoff, heuristic)

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
def idastar(matrix, heuristic):
  initial_time = time.process_time()
  process = psutil.Process(os.getpid())
  initial_memory = process.memory_info().rss / 1024.000000
  
  # initialization
  path = []
  cutoff = 0
  expanded_nodes = []
  global explored_nodes
  explored_nodes = []

  # set cutoff
  if (heuristic == 'h1'):
    cutoff = h1_misplaced_tiles(matrix)
  else:
    cutoff = h2_manhattan_distance(matrix)

  root = Node(matrix)
  path.insert(0, root)

  iterations = 0

  while True:
    explored_nodes = []

    iterations += 1

    # begin searching
    temp = search(path, 0, cutoff, heuristic)

    if (temp == 'found'):
      print('\nSolved in', iterations, 'iterations using', heuristic)
      elapsed_time = time.process_time() - initial_time
      final_memory = process.memory_info().rss / 1024.000000
      memory_used = final_memory - initial_memory
      print_search_info(path[0], len(explored_nodes), elapsed_time, memory_used)
      return path[0]

    # no solution
    if (temp == float('inf')):
      print('This algorithm was not able to find a solution')
      return

    # increase cutoff
    cutoff = temp
    




       
def main():
  print('------------------------------------------')
  print('| 15 Puzzle using Iterative Deepening A* |')
  print('------------------------------------------')

  #print('\nEnter \'h\' any time to swich heuristics.')

  #heuristic = get_heuristic()

  input = get_user_input()
  
  
  matrix = get_matrix(input)
  
  print('\n\nIDA* using h...')
  node = idastar(matrix, 'h1')

  print('\n\nIDA* using h2...')
  node = idastar(matrix, 'h2')

    
  





if __name__ == '__main__':
  main()    
    
    
    
     
