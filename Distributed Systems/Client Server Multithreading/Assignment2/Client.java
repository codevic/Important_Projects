import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

public class Client {

	private static Socket socket;
	private static DataInputStream in;
	private static DataOutputStream out;
	private static BufferedReader br;
//	static ClientServerThread csThread;

	public static void main(String[] args) throws Exception {
		try{
			socket=new Socket("127.0.0.1",7777);
			in=new DataInputStream(socket.getInputStream());
			out=new DataOutputStream(socket.getOutputStream());
			br=new BufferedReader(new InputStreamReader(System.in));
			String clientMsg="",serverMsg="";
			clientMsg=menu();
			if(clientMsg.equals("1") || clientMsg.equals("2") || clientMsg.equals("3") || clientMsg.equals("4"))
			{	out.writeUTF(clientMsg);
			out.flush();
			serverMsg=in.readUTF();
			System.out.println(serverMsg);
			clientMsg = br.readLine();
			out.writeUTF(clientMsg);
			out.flush();
			serverMsg=in.readUTF();
			System.out.println(serverMsg);				
		}
		else if(clientMsg.equals("5")){
			System.out.println("\nExiting...");
		}
		else {
			System.out.println("\n You typed the wrong choice.");
		}
		System.exit(0);		
		/*		System.out.println("C : choice "+clientMsg+". passing it...");
				out.writeUTF(clientMsg);
				System.out.println("C : passed!");
				out.flush();
				System.out.println("C : Reading from server!");
				serverMsg=in.readUTF();
				System.out.println(serverMsg);
				String filename = br.readLine();
				out.writeUTF(filename);
				out.flush();	
				System.out.println("C : Ending client"); */
			//}
			out.close();
			out.close();
			socket.close();
		}catch(Exception e){
			System.out.println(e);
		}
	}

	public static String menu() throws IOException {
		System.out.println("\nSelect an action to do : ");
		System.out.println("For Uploading a File, type 1 followed by the name of the file to be uploaded : 1 filename.txt");
		System.out.println("For Downloading a File, type 2 followed by the name of the file to be downloaded : 2 filename.txt");
		System.out.println("For Renaming a File, type 3 followed by the name of the file to be renamed and the new name : 3 filename.txt new_name.txt");
		System.out.println("For Deleting a File, type 4 followed by the name of the file to be deleted : 4 filename.txt");
		System.out.print("\nPress a key (1-4): ");
		String choice = br.readLine();
		return choice;
	}
}