import java.net.*;
import java.io.*;

public class Server {

	public static void main(String[] args) throws Exception {

		try{

			ServerSocket serverSocket=new ServerSocket(6666);
			Socket clientSocket=serverSocket.accept();
			DataInputStream in=new DataInputStream(clientSocket.getInputStream());
			DataOutputStream out=new DataOutputStream(clientSocket.getOutputStream());
			String clientMsg = null, serverMsg, filename;
			int cmsgParse = 0;
			clientMsg=in.readUTF();
			if(clientMsg.equals("1") || clientMsg.equals("2") || clientMsg.equals("3") || clientMsg.equals("4")) {
				cmsgParse = Integer.parseInt(clientMsg) ;
				switch(cmsgParse) {
				case 1: 
					serverMsg="\nYou have chosen to Upload a file!\n Provide the name of the file you want to upload : ";
					out.writeUTF(serverMsg);
					filename = in.readUTF();
					if(uploadFile(filename))
						serverMsg="\n File successfully uploaded to the serverSocket!";
					else
						serverMsg="\n File could not be uploaded to the serverSocket!";
					out.writeUTF(serverMsg);
					System.exit(0);
					break;
				case 2:
					serverMsg="\nYou have chosen to Download a file!\n Provide the name of the file you want to download : ";
					out.writeUTF(serverMsg);
					filename = in.readUTF();
					if(downloadFile(filename))
						serverMsg="\n File successfully downloaded to the serverSocket!";
					else
						serverMsg="\n File could not be downloaded to the serverSocket!";
					out.writeUTF(serverMsg);
					System.exit(0);
					break;
				case 3:
					serverMsg="\nYou have chosen to Rename a file!\n Provide the name of the file you want to rename and "
							+"also the new name with a space.\n Like FileName newFileName: ";
					out.writeUTF(serverMsg);
					filename = in.readUTF();
					String[] inputs = filename.split(" ");
					if(renameFile(inputs[0],inputs[1]))
						serverMsg="\n File successfully renamed in the serverSocket!";
					else
						serverMsg="\n File could not be renamed in the serverSocket!";
					out.writeUTF(serverMsg);
					System.exit(0);
					break;
				case 4:
					serverMsg="\nYou have chosen to Delete a file!\n Provide the name of the file you want to delete : ";
					out.writeUTF(serverMsg);
					filename = in.readUTF();
					if(deleteFile(filename))
						serverMsg="\n File successfully deleted from the serverSocket!";
					else
						serverMsg="\n File could not be deleted from the serverSocket!";
					out.writeUTF(serverMsg);
					System.exit(0);
					break;
				default:
					System.out.println("\nYou pressed the wrong choice!");
					System.exit(0);
					break;
				}
			}
			in.close();
			out.close();
			clientSocket.close();
			serverSocket.close();
		}catch(Exception e){
			System.out.println(e);
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