import java.io.*;
import java.util.*;
import java.lang.*;
import java.net.*;
import sun.net.*;
 
public class Process2{
              // initializing daemon to 0
              public static int daemon = 0;
              static boolean SyncAll = false;
              public static void main(String args[]) throws Exception
              {
                            // creating thread
                           final Process2Thread process = new Process2Thread();
                           // get time from daemon
                           process.ReceiveTime();
                           Thread Synchronization = new Thread()
                           {
                                         public void run()
                                         {
                                                       try{
                                                                    process.SynchronizeProcess();
                                                      } catch (Exception e) {
                                                                    e.printStackTrace();
                                                       }
                                         }
                           };
                           Thread Send = new Thread()
                           {
                                         public void run()
                                         {
                                                       try{
                                                                    process.SendMessage();
                                                       } catch(Exception e) {
                                                                    e.printStackTrace();
                                                       }
                                         }
                           };
                                        
                           Thread Receive = new Thread()
                           {
                                         public void run()
                                         {
                                                       try{
                                                                    process.ReceiveMessage();
                                                       } catch(Exception e) {
                                                                    e.printStackTrace();
                                                       }                                                    
                                         }
                           };
                           // Synchronize with daemon
                           Synchronization.start();
                           // Send and Receive messages
                           Send.start();
                           Receive.start();
              }
}
 
class Process2Thread {              
              static boolean syncAll = false;
              // initializing count to a random int
              int count = new Random().nextInt(30)+1;
              int drift = 0, nodes = 0, pid = 0;
              boolean synched = false;
              String message = new String();

             // method to retrieve time and difference from daemon
              public void ReceiveTime() throws Exception
              {
                           InetAddress group = InetAddress.getByName("224.0.0.7");
                           MulticastSocket Socket1 = new MulticastSocket(4444);
                           MulticastSocket Socket2 = new MulticastSocket(4445);
                           Socket1.joinGroup(group);
                           byte[] msgBuf = new byte[1000];
                           DatagramPacket dataPacket = new DatagramPacket(msgBuf, msgBuf.length);
                           Socket1.receive(dataPacket);
                           String message = new String(dataPacket.getData(),0,dataPacket.getLength());
                           int daemonCount = Integer.parseInt(message);
                           int difference = count - daemonCount;
                           message = Integer.toString(difference);
                           DatagramPacket dataPacket1 = new DatagramPacket(message.getBytes(), message.length(),group, 4445);
                           Socket2.send(dataPacket1);                 
              }

             // method to Synchronize the process with respect to the daemon time
              public void SynchronizeProcess() throws Exception
              {
                           InetAddress group = InetAddress.getByName("224.0.0.7");
                           MulticastSocket Socket2 = new MulticastSocket(4444);
                           byte[] msgBuf = new byte[1000];
                           DatagramPacket dataPacket = new DatagramPacket(msgBuf, msgBuf.length);
                           Socket2.joinGroup(group);
                           while(!syncAll)
                           {
                                         Socket2.receive(dataPacket);
                                         String message = new String(dataPacket.getData(),0,dataPacket.getLength());
                                         String[] sync = message.split(":");
                                         if(sync.length==4){
                                                       if(!synched){
                                                                    count = Integer.valueOf(sync[1])+count;
                                                                    pid = Integer.valueOf(sync[2]);
                                                       nodes = Integer.valueOf(sync[3]);
                                                       synched = true;
                                                       System.out.println();
                                                       if(pid == nodes)
                                                       {
                                                                    syncAll = true;
                                                       }
                                                       }           
                                                       else{
                                                                    count = Integer.valueOf(sync[0]) + count;
                                                                    if(Integer.valueOf(sync[2])==nodes)
                                                                                  syncAll= true;
                                                       }
                                         }
                           }
              }
                          
             // method to Send message to processes
              public void SendMessage() throws Exception
              {
                           String message = "";
                           InetAddress group = InetAddress.getByName("224.0.0.7");
                           MulticastSocket Socket1 = new MulticastSocket(4445);
                           while(!syncAll)
                                         Thread.sleep(5000);
                           System.out.println("Sending messages...");
                           System.out.println();
                           for(int i=0;i<2;i++)
                           {
                                         Thread.sleep(new Random().nextInt(3000)+1000);
                                         message = "Message "+i+" from Process "+pid;
                                         DatagramPacket dataPacket = new DatagramPacket(message.getBytes(), message.length(),group, 4445);
                                         Socket1.send(dataPacket);
                           }                                       
              }
             // method to Receive message from processes
              public void ReceiveMessage() throws Exception
              {
                           String message = "";
                           InetAddress group = InetAddress.getByName("224.0.0.7");
                           MulticastSocket Socket2 = new MulticastSocket(4445);
                           Socket2.joinGroup(group);
                           byte[] msgBuf = new byte[1000];
                           DatagramPacket dataPacket = new DatagramPacket(msgBuf, msgBuf.length);
                           while(!syncAll)
                                         Thread.sleep(5000);
                           System.out.println("Receiving messages...");            
                           while(true)
                           {
                                         Socket2.receive(dataPacket);
                                         message = new String(dataPacket.getData(),0,dataPacket.getLength());
                                         if(message.length()>15)
                                                       System.out.println("Received "+message);
                           }
              }
}
