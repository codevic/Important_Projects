import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class ClientServerThread extends Thread {

	static Socket serverClient;
	int clientID;
	String Filename;

	ClientServerThread(Socket inSocket,int counter){
		serverClient = inSocket;
		clientID=counter;
	}
	public void run(){
		try{
			System.out.println("In Server Client Thread");
			DataInputStream in = new DataInputStream(serverClient.getInputStream());
			DataOutputStream out = new DataOutputStream(serverClient.getOutputStream());
			String clientMsg, serverMsg;
			clientMsg=in.readUTF();
			while(!clientMsg.equals("5")){
				String[] inputs = clientMsg.split(" ");
				String renameTo = null;
				if(inputs.length > 1)
				{
					Filename = inputs[1];
					if(inputs.length>2)
						renameTo = inputs[2];
				}
				switch(Integer.parseInt(inputs[0])) {
				case 1:
					serverMsg="\nYou have chosen to Upload a file! Provide the name of the file";
					out.writeUTF(serverMsg);
					Filename = in.readUTF();
					uploadFile(Filename);
					break;
				case 2:
					serverMsg="\nYou have chosen to Download the file! Provide the name of the file";
					out.writeUTF(serverMsg);
					Filename = in.readUTF();
					downloadFile(Filename);
					break;
				case 3:
					serverMsg="\nYou have chosen to Rename a file! Provide the name of the file you want to rename and "
							+"also the new name with a space.\n Like FileName newFileName";
					out.writeUTF(serverMsg);
					Filename = in.readUTF();
					String[] input = Filename.split(" ");
					if(renameFile(input[0],input[1]))
						serverMsg="\n File successfully renamed in the serverSocket!";
					else
						serverMsg="\n File could not be renamed in the serverSocket!";
					out.writeUTF(serverMsg);
					break;
				case 4:
					serverMsg="\nYou have chosen to Delete a file! Provide the name of the file";
					out.writeUTF(serverMsg);
					Filename = in.readUTF();
					deleteFile(Filename);
					break;
				case 5:
					System.exit(0);
					break;
				default:
					System.out.println("\nYou pressed the wrong choice!");
					break;
				}
				//   squre = Integer.parseInt(clientMsg) * Integer.parseInt(clientMsg);
				serverMsg="Done!";
				out.writeUTF(serverMsg);
				out.flush();
			}
			in.close();
			out.close();
			serverClient.close();
		}catch(Exception ex){
			//System.out.println(ex);
		}finally{
			System.out.println("Client -" + clientID + " exit!! ");

		}
	}


	private static boolean deleteFile(String filename) {
		String fullFile = filename+".txt";
		File file = new File(fullFile);
		boolean deleted = file.delete();
		if(deleted) {
			System.out.println("File "+fullFile+" Deleted from Server by Client.");
			return true;
		}			
		else
			return false;
	}

	private static boolean renameFile(String filename, String renameTo) {
		String fullFile = filename+".txt";
		String newFull = renameTo+".txt";
		File file = new File(fullFile);
		File newFile = new File(newFull);
		if(file.renameTo(newFile)){
			System.out.println("File "+fullFile+" Renamed to "+newFull+" by Client.");
			return true;
		}else{
			return false;
		}
	}

	private static boolean downloadFile(String filename) {
		String file = filename+".txt";
		try {

			InputStream in = new FileInputStream(file);
			OutputStream out = new FileOutputStream(filename+"-DownloadedFromServer.txt");

			byte[] buffer = new byte[1024];
			int len;
			while ((len = in.read(buffer)) > 0) {
				out.write(buffer, 0, len);
			}
			in.close();
			out.close();
			System.out.println("File "+file+" Downloaded from Server by Client.");
			return true;
		} catch (IOException ex) {
			System.err.println("Connection closed due to client side error!");
		} catch (NumberFormatException e) {
			e.printStackTrace();
		}
		return false;
	}

	private static boolean uploadFile(String filename) {
		String file = filename+".txt";
		try {

			InputStream in = new FileInputStream(file);
			OutputStream out = new FileOutputStream(filename+"-UploadedByClient.txt");

			byte[] buffer = new byte[1024];
			int len;
			while ((len = in.read(buffer)) > 0) {
				out.write(buffer, 0, len);
			}
			in.close();
			out.close();
			System.out.println("File "+file+" Uploaded to Server by Client.");
			return true;
		} catch (IOException ex) {
			System.err.println("Connection closed due to client side error!");
		}
		return false;
	}
}                 