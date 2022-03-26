LAB_2: Python 3.9, Creating random graphs and finding hamiltonian and eulerian cycles
=

graph_creator.py: 
-

Creates random related undirected graph and save it in graph.bin
   
- Usage: python3 graph_creator.py -V 6 -E 10 -S


- flags: 
  - -V [number_of_vertexes ] - how many vertexes will be in graph, by default = 5
  - -E [number_of_edges]     - how many edges will be in graph, by default = random from V - 1 to 2 * V 
  - -S                       - program will save image of the graph in graph.png 

  
- Output:
  - ./graph.bin              - edges of the graph in binary format
  - ./graph.png (optional)   - graph image, created with networkx and matplotlib.pyplot
    
main.py:
-
Finds and outputs (if there is) an Euler or Hamilton cycle

- Usage: python3 main.py -E graph.bin -S


- flags: 
  - -E / -H                  - What cycle do you want to find: -E - Eulerian, -H - Hamiltonian
  - path to bin file         - Path to the binary file with graph created by graph_creator.py   
  - -S                       - The program will save the image of the graph with the directions of the cycle 


- Output:
  - ./Eulerian_cycle.png (optional)    - Eulerian cycle image, created with networkx and matplotlib.pyplot
  - ./Hamiltonian_cycle.png (optional) - Hamiltonian cycle image
  

Files structure
-

graph.bin
-
- a utf-8 binary file with a structure where each line encodes one edge:
  
      node_name + ' ' + node_name + '\n'
      node_name + ' ' + node_name + '\n'
      node_name + ' ' + node_name + '\n'
      node_name + ' ' + node_name + '\n'

    *node_name is an integer
    