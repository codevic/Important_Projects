************************************************************************************
Program Structure :

The zip file contains three Java classes namely, Node, Edge and find_route.

The map is created as a graph. Every node is the city and it's connecting cities are edges.

Node.java defines the characteristics of a city, i.e, its name, its parent node, its edges and the pathCost. The constructor, getter and toString() methods are defined. Additionally, the method insertEdge() adds an edge to the node, calculateCost() method calculates the cost from the node to it's parent, compare() method compares nodes to prioritise them according to their cost and an overriden equals() method compares the Node object's value with one another.

Edge.java defines the characterisitics of every city connected to a particular city(Node). Hence it has a node(destination city) and the cost to reach that city. The constructor, getter and toString() methods are defined.

find_route.java reads the command line arguments. It takes in three arguments namely, input filename, origin city and destination city. 
 > The createGraph(filename) method reads the file line by line to create a grap (map) using the Node and Edge class and returns it(graph).
 > finds and assigns the origin and destination Node.
 > UniformCostSearch(origin, destination) method implements the uniform cost search  algorithm to find the shortest path from the origin node and destination node.
 > Generates path
 > Prints out distance and route, if exists

************************************************************************************

How to run :

The program takes exactly three arguments.

Example,
	find_route input_filename origin_city destination_city

To compile the program,
	javac find_route.java

To run the program,
	java find_route input1.txt Bremen Frankfurt

  The input1.txt is already present in the directory as a sample input to work with.
  
  This program will then compute the shortest route between the two cities, calculate the cost and display the distance and route with the cities that fall in the route.

Example, for input, java find_route input1.txt Bremen Frankfurt,

Output will be,
distance: 455 km
route:
Bremen to Dortmund, 234 km
Dortmund to Frankfurt, 221 km

  If there is no route between the provided two cities the distance will be displayed as infinity and route as none.

Example, for input, java find_route input1.txt London Frankfurt,

Output will be,
distance: infinity
route:
none

************************************************************************************