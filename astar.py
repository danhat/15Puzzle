

from helperfunctions import *
  




"""
    Function to solve 15 puzzle using a*.
    
    Arguments:
        4 by 4 matrix
        heuristic type
          'h1' or 'h2'
    Returns:
        goal state node (unless program exits due to an empty open list)
"""
def astar(matrix, heuristic_type, return_info): 
  process = psutil.Process(os.getpid())
  initial_memory = process.memory_info().rss / 1024.000000

  initial_time = time.process_time()

  # head node
  initial_node = Node(matrix) 
  
  initial_node.g_n = 0
  initial_node.f_n = 0
  open_list = []
  closed_list = []

  open_list.append(initial_node)
  
  expanded_nodes_count = 0

  
  while (len(open_list) > 0):
    timed_out = time.process_time() - initial_time
    if (timed_out > 10):
      print('\n**A* timed out**')
      return
    pop_index = 0

    i = 0
    # get index of the node with the lowest f(n)
    while (i < len(open_list)):
      if (open_list[i].f_n < open_list[pop_index].f_n):
        pop_index = i
      i += 1

    # pop node with the lowest f(n)
    node = open_list.pop(pop_index)

    expanded_nodes_count = expanded_nodes_count + 1
    
    if(node.matrix == goal_matrix):
      # stop time and memory after bfs returns
      elapsed_time = time.process_time() - initial_time
      final_memory = process.memory_info().rss / 1024.000000
      memory_used = final_memory - initial_memory
      if (return_info == True):
        return (node, expanded_nodes_count, elapsed_time, memory_used)
      else:
        print_search_info(node, expanded_nodes_count, elapsed_time, memory_used)
        return node


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
    children = get_children(node, [])

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
        for n in closed_list:
          if (child == n):
            continue

        # child is already in open with lower g(n)
        for n in open_list:
          if (child.matrix == n.matrix and child.f_n > n.f_n):
            continue

        open_list.append(child)

    closed_list.append(node)

  # open is empty, no solution found
  print('A* failed to find a solution.')
    
        
        
       
def main():
  print('\n15 Puzzle using A*\n')

  input = get_user_input()    
  matrix = get_matrix(input)
    
  
  
  print('\nA* using h1...')
  node = astar(matrix, 'h1', False)


  print('\n\nA* using h2...')
  node = astar(matrix, 'h2', False)
  #node = astar(matrix, 'h2', True)
  #print(node[1])

  

if __name__ == '__main__':
  main()    
    
    
    
    
    
    
    
    
    
    
    
    
    
