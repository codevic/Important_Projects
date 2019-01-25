import java.net.*;
import sun.net.*;
import java.util.*;
import java.io.*;

public class Daemon2{
             
              public static void main(String[] args) throws Exception
              {
                           Scanner sc = new Scanner(System.in);
                           final Daemon2Thread dThread = new Daemon2Thread();
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

class Daemon2Thread{
              int count = new Random().nextInt(30)+1;
              String message = new String();
              boolean syncAll = false;
              int drift = 0, numNodes = 1, offset = 0, check = 0;
 
              public void SendMessage() throws Exception{
                           System.out.println("\nServer initiated and listening...");
                           InetAddress group = InetAddress.getByName("224.0.0.7");              
                           MulticastSocket Socket1 = new MulticastSocket(4444);
                           while(!syncAll)
                           {
                                         message = Integer.toString(count);
                                         Socket1.send(new DatagramPacket(message.getBytes(), message.length(),group, 4444));                      
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
                                         drift = difference/numNodes;                                                      
                                         offset = drift - difference;       
                                         message = drift+":"+offset+":"+ID+":"+check;
                                         count += drift;
                                         System.out.println();
                                         Thread.sleep(1000);
                                         Socket2.send(new DatagramPacket(message.getBytes(), message.length(),group, 4444));
                            }
              }
             
              public void nodeCount(int num) throws Exception{
                           check  = num;
              }
}
