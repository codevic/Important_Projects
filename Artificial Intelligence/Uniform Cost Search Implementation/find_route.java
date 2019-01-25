
import java.util.Collections;
import java.util.List;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.PriorityQueue;
import java.util.HashSet;

public class find_route {

	// Reads the input file line by line and creates and returns a map(graph)
	public static ArrayList<Node> createGraph(String filename) {
		ArrayList<Node> map = new ArrayList<Node>();
		File file = new File(filename);
		// Read file line by line
		try {
			InputStream in = new FileInputStream(file);
			BufferedReader br = new BufferedReader(new InputStreamReader(in));
			String line;
			while ((line = br.readLine()) != null) {
				// Check for "END OF INPUT" String. If found, exit.
				if (line.equals("END OF INPUT"))
					break;
				// Split line and assign the values appropriately to the nodes and their costs.
				String[] values = line.split(" ");
				String origin_city = values[0].toString();
				String destination_city = values[1].toString();
				int cost = Integer.parseInt(values[2]);

				// Initialize the nodes: origin and destination
				Node origin = new Node(origin_city);
				Node destination = new Node(destination_city);
				int index = -1;

				// If graph already has the origin_city, then get its index.
				// Assign it to the current origin_city.
				if (map.contains(origin) == true) {
					index = getIndex(origin, map);
					origin = map.get(index);
				}

				// If graph already has the destination_city, then get its index.
				// Assign it to the current destiantion_city.
				// Add a new edge connecting to the origin with its cost value.
				// Else, add new edge to the new destination.
				// Add the new destination the graph.
				if (map.contains(destination) == true) {
					index = getIndex(destination, map);
					destination = map.get(index);
					destination.insertEdge(origin, cost);
					index = getIndex(destination, map);
					map.set(index, destination);
				} else {
					destination.insertEdge(origin, cost);
					map.add(destination);
				}

				// Add edge from origin to destination with cost value.
				origin.insertEdge(destination, cost);

				// If graph already has origin_city, then set the index to the current
				// origin_city.
				// Else, add the new origin_city to the graph

				if (map.contains(origin) == true) {
					index = getIndex(origin, map);
					map.set(index, origin);
				} else {
					map.add(origin);
				}
			}
			br.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (NumberFormatException e) {
			System.out.println("Reached End of Line");
		} catch (IOException e) {
			e.printStackTrace();
		}
		return map;
	}

	// Uniform Cost Search Algorithm Implementation
	public static void UniformCostSearch(Node origin, Node destination) {
		// Set path cost of the initial state, i.e.,
		// the origin node, to 0.
		origin.pathCost = 0;

		// Create the frontier_queue (PriorityQueue)
		PriorityQueue<Node> frontier_queue = new PriorityQueue<Node>(25, origin);
		// Add the origin node to the frontier
		frontier_queue.add(origin);
		Node current = null;

		// explored consists of the already visited nodes
		HashSet<Node> explored = new HashSet<Node>();

		// loop
		do {
			// set origin as the current node initially.
			current = frontier_queue.poll();
			// add the node to explored set, as it is considered visited
			explored.add(current);
			// For every edge found for that origin node
			for (Edge e : current.toCity) {
				// set child node as destination and set current cost to it's cost
				Node child = e.destination;
				int cost = e.cost;
				// if child is not present in the frontier queue,
				// then add the cost of the child node to the path cost
				// if child is not present in the explored set,
				// then set parent node to current and add child to frontier queue
				// else if child is present in frontier queue and child's path cost is greater
				// than sum of current path cost and cost, then set parent to current and add
				// child to frontier queue
				if (frontier_queue.contains(child) == false) {
					child.pathCost = current.pathCost + cost;
					if (explored.contains(child) == false) {
						child.parent = current;
						frontier_queue.add(child);
					}
				} else if ((frontier_queue.contains(child) == true) && (child.pathCost > current.pathCost + cost)) {
					child.parent = current;
					frontier_queue.remove(child);
					frontier_queue.add(child);
				}
			}
		} while (frontier_queue.isEmpty() == false);
	}

	// Returns the index of the node
	private static int getIndex(Node node, ArrayList<Node> graph) {
		for (int i = 0; i < graph.size(); i++)
			if (graph.get(i).toString().equals(node.toString()))
				return i;
		return -1;
	}

	public static void main(String[] args) {
		
		// Check if arguments are provided
		if (args.length < 3) { System.out.println("Wrong arguments"); System.exit(0);
		}
		
		// Create graph using the input file given
		ArrayList<Node> graph = createGraph(args[0]);
		//"K:\\UTA\\Fall 2017\\CSE 5360 - Artificial Intelligence 1\\Assignments\\A1 - UninformedSearch\\src\\uninformedsearch\\input1.txt");
		Node origin = null, destination = null;
		// Find the origin and destination node in the graph and assign them.
		for (Node node : graph) {
			if (node.toString().equals(args[1].toString()))//"Bremen"))
				origin = node;
			else if (node.toString().equals(args[2].toString()))//"Frankfurt"))
				destination = node;
		}
		int distance = 0;
		
		// Implement Uniform Cost Search to find the shortest path between the given origin and destination
		UniformCostSearch(origin, destination);
		
		// Get the route
		List<Node> route = new ArrayList<Node>();
		for (Node node = destination; node != null; node = node.parent)
			route.add(node);
		Collections.reverse(route);
		
		// Calculate the distance 
		for (Node node : route) {
			if (node.parent != null)
				distance += node.calculateCost();
		}
		
		// if distance is greater than 0, then print distance and route
		// else, print distance as infinity and route as none.
		if (distance > 0) {
			System.out.println("distance: " + distance + " km");
			System.out.println("route: ");
			for (Node node : route) {
				if (node.parent != null)
					System.out.println(node.parent + " to " + node + ", " + node.calculateCost() + " km");
			}
		} else {
			System.out.println("distance: infinity");
			System.out.println("route: ");
			System.out.print("none");
		}
	}
}