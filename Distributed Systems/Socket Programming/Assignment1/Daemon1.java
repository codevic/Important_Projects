import java.net.*;
import sun.net.*;
import java.util.*;
import java.io.*;
 
public class Daemon1{
             
              public static void main(String[] args) throws Exception
              {
                           Scanner sc = new Scanner(System.in);
                           final Daemon1Thread dThread = new Daemon1Thread();
                           int numOfNodes = 3;
                           dThread.nodeCount(numOfNodes);
                           Thread Send = new Thread()
                           {
                                         public void run()
                                         {
                                                       try{
                                                                    dThread.ReceiveMessage();
                                                       } catch(Exception e){
                                                                    e.printStackTrace();
                                                       }
                                         }
                           };
                                        
                           Thread Receive = new Thread()
                           {
                                         public void run()
                                         {
                                                       try{
                                                                    dThread.SendMessage();
                                                       } catch(Exception e){
                                                                    e.printStackTrace();
                                                       }                                                    
                                         }
                           };
                           Send.start();
                           Receive.start();
              }
}
class Daemon1Thread{
              int count = new Random().nextInt(30)+1;
              String message = new String();
              boolean syncAll = false;
              int drift = 0, numNodes = 1, offset = 0, check = 0;
 
              public void SendMessage() throws Exception{
                           System.out.println("The count is : "+count);
                           InetAddress group = InetAddress.getByName("224.0.0.7");              
                           MulticastSocket Socket1 = new MulticastSocket(4444);
                           while(!syncAll)
                           {
                                         message = Integer.toString(count);    
                                         DatagramPacket hi = new DatagramPacket(message.getBytes(), message.length(),group, 4444);
                                         Socket1.send(hi);                      
                                         Thread.sleep(3000);
                           }
              }
 
              //for receiving the offset from the slave numNodes and calculating the average
              public void ReceiveMessage() throws Exception {
                           byte[] msgBuf = new byte[1000];
                           InetAddress group = InetAddress.getByName("224.0.0.7");              
                           MulticastSocket Socket1 = new MulticastSocket(4445);
                           MulticastSocket Socket2 = new MulticastSocket(4444);
                           DatagramPacket dataPacket = new DatagramPacket(msgBuf, msgBuf.length);
                           Socket1.joinGroup(group);
                           while(!syncAll)
                           {
                                         Socket1.receive(dataPacket);
                                         String message = new String(dataPacket.getData(),0,dataPacket.getLength());
                                         System.out.println("A new client has been generated");
                                         int ID = numNodes;
                                         if(numNodes==check)
                                                       syncAll = true;
                                         numNodes++;
                                         int difference = Integer.valueOf(message);
                                         System.out.println("The offset of "+difference+" received.");
                                         drift = difference/numNodes;                                                      
                                         offset = drift - difference;       
                                         message = drift+":"+offset+":"+ID+":"+check;
                                         System.out.println("Calcualted the average.");
                                         count += drift;
                                         System.out.println("Updated count : "+count);
                                         System.out.println("Now sending the new offset to the client nodes...");
                                         System.out.println();
                                         Thread.sleep(1000);
                                         Socket2.send(new DatagramPacket(message.getBytes(), message.length(),group, 4444));
                            }
              }
             
              public void nodeCount(int num) throws Exception{
                           check  = num;
              }
}
