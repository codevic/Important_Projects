import sun.net.*;
import java.io.*;
import java.net.*;
import java.util.*;
import java.lang.*;
 
public class Process1{              
              static boolean SyncAll = false;
              // initializing daemon to 0
              public static int daemon = 0;
              public static void main(String args[]) throws Exception
              {
                          // creating thread
                           final Process1Thread process = new Process1Thread();
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
                           // Synchronize with daemon
                           Synchronization.start();
              }
}
 
class Process1Thread {              
              static boolean syncAll = false;
              // initializing count to a random int
              int count = new Random().nextInt(30)+1;
              int drift = 0, nodes = 0, pid = 0;
              boolean synched = false;
              String message = new String();
             
             // method to retrieve time and difference from daemon
              public void ReceiveTime() throws Exception
              {
                           System.out.println("The count is : "+count);
                           InetAddress group = InetAddress.getByName("224.0.0.7");
                           MulticastSocket Socket1 = new MulticastSocket(4444);
                           MulticastSocket Socket2 = new MulticastSocket(4445);
                           Socket1.joinGroup(group);
                           byte[] msgBuf = new byte[1000];
                           DatagramPacket dataPacket = new DatagramPacket(msgBuf, msgBuf.length);
                           Socket1.receive(dataPacket);
                           String message = new String(dataPacket.getData(),0,dataPacket.getLength());
                           int daemonCount = Integer.parseInt(message);
                           System.out.println("The daemon count is :"+daemonCount);
                           int difference = count - daemonCount;
                           System.out.println("The Offset of "+difference+" sent to the time daemon.");
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
                                                                    System.out.println("Received a new offset.");
                                                                    System.out.println("Synchronizing with the time daemon....");
                                                                    count = Integer.valueOf(sync[1])+count;
                                                                    pid = Integer.valueOf(sync[2]);
                                                       nodes = Integer.valueOf(sync[3]);
                                                       System.out.println("Updated count : "+count);
                                                       System.out.println("The Client process is assigned pid : "+pid);
                                                       synched = true;
                                                       System.out.println();
                                                       if(pid == nodes)
                                                       {
                                                                    syncAll = true;
                                                       }
                                                       }           
                                                       else{
                                                                    System.out.println("Received a new offset.\n Offset : "+sync[0]);
                                                                    System.out.println("Synchronizing with the new average...");
                                                                    count = Integer.valueOf(sync[0]) + count;
                                                                    System.out.println("Synchronized.\n The new count is : "+count);         
                                                                     System.out.println();
                                                                    if(Integer.valueOf(sync[2])==nodes)
                                                                                  syncAll= true;
                                                       }
                                         }
                           }
              }
              
             
}