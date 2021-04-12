

from helperfunctions import *



"""
  Function to solve 15 puzzle using bfs.
    
  Arguments:
    4 by 4 matrix
  Returns:
    goal state node (unless program exits due to an empty queue)
"""
def bfs(matrix, return_info): 
  # start timer 
  initial_time = time.process_time()
  
  process = psutil.Process(os.getpid())
  initial_memory = process.memory_info().rss / 1024.000000
  
  expanded_nodes = []
  expanded_nodes_count = 0

  # head node
  initial_node = Node(matrix) 


  # check to see if initial matrix is the goal state
  # if so, return that node
  if (initial_node.matrix == goal_matrix):
    # stop time when goal matrix is found
    elapsed_time = time.process_time() - initial_time
    # get memory usage
    final_memory = process.memory_info().rss / 1024.000000
    memory_used = final_memory - initial_memory
    if (return_info == True):
      return (initial_node, expanded_nodes_count, elapsed_time, memory_used)
    else:
      print_search_info(initial_node, expanded_nodes_count, elapsed_time, memory_used)
      return initial_node
    
  # initialize queue and enqueue head node
  q = Queue()
  q.put(initial_node)  

  while True:
    timed_out = time.process_time() - initial_time
    if (timed_out > 3):
      print('\n**BFS timed out**')
      return

    # if queue is empty, no solution is able to be found using this program
    if(q.empty() == True):
      print('BFS failed to find a solution.')
      return
        
    # get node at the front of queue
    node = q.get()
        
    # if node has not been expanded yet, add it to expanded nodes
    if (expanded_nodes.__contains__(node.matrix) == False):
      expanded_nodes.append(node.matrix)
      expanded_nodes_count += 1
        
    children = get_children(node, expanded_nodes)

    for child in children:
      if (child.matrix == goal_matrix):
        # stop time when goal matrix is found
        elapsed_time = time.process_time() - initial_time
        # get memory usage
        final_memory = process.memory_info().rss / 1024.000000
        memory_used = final_memory - initial_memory
        if (return_info == True):
          return (child, expanded_nodes_count, elapsed_time, memory_used)
        else:
          print_search_info(child, expanded_nodes_count, elapsed_time, memory_used)
        return False
        #return child
      if (child.matrix != None):
        q.put(child)
        
    
        
    
    
def main():
  

  input = get_user_input()     
    
  print('\n15 Puzzle using BFS')
   
  matrix = get_matrix(input)

  print('\nInitial State: \n')

  print_matrix(matrix)
  print('\n')
    
  node = bfs(matrix, False)


if __name__ == '__main__':
  main()    
    
    
    
    
    
    
    
    
    
    
    
    
    
