
public class Edge {
	
	// Public member variables
	public final Node destination;
	public final int cost;
	
	// Constructor
	public Edge(Node destinationNode, int cost_value) {
		cost = cost_value;
		destination = destinationNode;
	}
	
	// Getter methods
	public double getCost() {
		return cost;
	}
	public Node getDestination() {
		return destination;
	}

	// toString method
	public String toString() {
		return destination.toString();
	}
}
