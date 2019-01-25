import java.net.ServerSocket;
import java.net.Socket;

public class MultithreadedServerSocket {
	public static void main(String[] args) throws Exception {
             try{
                     ServerSocket server=new ServerSocket(7777);
                     int counter=0;
                     System.out.println("Server Started ....");
                     while(true){
                             counter++;
                             Socket serverClient=server.accept();  //server accept the client connection request
                             System.out.println(" >> " + "Client No:" + counter + " started!");
                             System.out.println(" S: lets start serverclientthread!!");
                             ClientServerThread csThread = new ClientServerThread(serverClient,counter); //send  the request to a separate thread
                             csThread.start();
                     }
             }catch(Exception e){
                     System.out.println(e);
             }
	}
}
