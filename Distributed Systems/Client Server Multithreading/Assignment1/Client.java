import java.net.*;
import java.io.*;

public class Client {

	private static BufferedReader br;

	public static void main(String[] args) throws Exception {

		try{
			
			Socket socket = new Socket("127.0.0.1",6666);
			DataInputStream in = new DataInputStream(socket.getInputStream());
			DataOutputStream out = new DataOutputStream(socket.getOutputStream());
			br = new BufferedReader(new InputStreamReader(System.in));
			String clientMsg ,serverMsg;
			clientMsg = menu();
			if(clientMsg.equals("1") || clientMsg.equals("2") || clientMsg.equals("3") || clientMsg.equals("4"))
			{
				out.writeUTF(clientMsg);
				out.flush();
				serverMsg=in.readUTF();
				System.out.println(serverMsg);
				clientMsg = br.readLine();
				out.writeUTF(clientMsg);
				out.flush();
				serverMsg=in.readUTF();
				System.out.println(serverMsg);				
			}
			else {
				System.out.println("\nYou typed the wrong command!");
			}
			System.exit(0);
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