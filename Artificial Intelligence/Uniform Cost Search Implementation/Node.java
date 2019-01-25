
import java.util.ArrayList;
import java.util.Comparator;

public class Node implements Comparator<Node> {
	
	// Public member variables
	public final String city;
	public ArrayList<Edge> toCity;
	public Node parent;
	public int pathCost;
	
	// Constructor
	public Node(String cityName) {
		city = cityName;
		toCity = new ArrayList<Edge>();
	}
	
	// Getter method
	public String toString() {
		return city;
	}
	
	// method to insert a new edge(city) to the node(city)
	public void insertEdge(Node destination, int cost) {
		Edge edge = new Edge(destination, cost);
		toCity.add(edge);
	}
	
	// method to calculate cost from that node to parent
	public int calculateCost() {
		for(Edge e : toCity) {
			if(e.destination.toString().equals(parent.toString())) 
				return e.cost;
		}
		return 0;
	}
	
	// Compare method for priority queue
	@Override
	public int compare(Node node1, Node node2){
        if(node1.pathCost < node2.pathCost)	return -1;
        else if (node1.pathCost > node2.pathCost)	return 1;
        else	return 0;
    }
	
	// Overridden equals method to support objects
	@Override
    public boolean equals(Object obj){
    	 if((obj instanceof Node) && city.equals(obj.toString()))
             return true;
         return false;
    }
}
