def print1():
	print('links \n')
	print('''
        https://drive.google.com/open?id=19ByejQR3OrZcKxpJW9bEv1G_EqwFBEj3
        http://www.mediafire.com/file/nix6dvjyrbidl77/NS2.rar/file
        https://filebin.net/q9c78zhpw0mq28al/NS2.rar?t=7h2nnef7
        https://file.io/youph2
''')
def print2():
	print('cdma \n')
	print('''from random import randrange
import numpy as np
user_rec={}
channel=[]
def createChannel(total_users):
    channel.clear()
    for i in range(0,total_users):
        sum=0
    for v in user_rec.values():
        sum+=v[i]
    channel.append(sum)
def makeChippingCode(user_no , bit , total_users):
    chipping=[]
    for i in range(0,total_users):
        chipping.append(randrange(-1,2))
    if user_rec: # check if dict has some data or not
        for k,v in user_rec.items():
            if v==tuple(chipping):
                makeChippingCode(user_no,bit,total_users) # If dict has same chipping
#code re calculate new one
            else:
                chipping=[(bit*i) for i in chipping]
                user_rec[user_no]=tuple(chipping)
                break
    else:
        chipping=[(bit*i) for i in chipping]
        user_rec[user_no]=tuple(chipping)
def getCommunicationData(Listening_node , Talking_node , total_users):
    print("Data of node {} is -> 1".format(Talking_node))
    if(sum(np.multiply(channel,user_rec[Talking_node]))/total_users>=0):
      print("Data of node {} is -> 0".format(Talking_node))
def inputs():
    total_users=int(input("Total number of users are -> "))
    for i in range(1,total_users+1):
        bit = int(input("Enter user {} data i.e (1 , -1) = ".format(i)))
    makeChippingCode(i,bit,total_users)
    createChannel(total_users)
    print("Data is channel is == ",tuple(channel))
    communication_nodes=input("Enter Who is Listening To Whom (e.g. 3 2) ?? =").split(" ")
    getCommunicationData(int(communication_nodes[0]),int(communication_nodes[1]),total_users)
#print("\n\n user_rec --> ",user_rec)
inputs()
''')
def print3():
	print('j2me \n')
	print('''package mypackage;
import java.io.IOException;
import javax.bluetooth.*;
import javax.bluetooth.DiscoveryListener;
import javax.microedition.lcdui.*;
import javax.microedition.midlet.*;
public class discover_device extends MIDlet implements CommandListener, DiscoveryListener {
 private final List deviceList;
 private final Command Exit, Refresh;
 private String deviceName;
 private DiscoveryAgent agent;
 private Alert dialog;
 public discover_device() {
  deviceList = new List( & quot; List of Devices & quot;, List.IMPLICIT);
  Exit = new Command( & quot; Exit & quot;, Command.EXIT, 0);
  Refresh = new Command( & quot; Refresh & quot;, Command.SCREEN, 1);
  deviceList.addCommand(Exit);
  deviceList.addCommand(Refresh);
  deviceList.setCommandListener(this);
  Display.getDisplay(this).setCurrent(deviceList);
 }
 public void startApp() {
  try {
   deviceList.deleteAll();
   LocalDevice local = LocalDevice.getLocalDevice();
   local.setDiscoverable(DiscoveryAgent.GIAC);
   deviceName = local.getFriendlyName();
   agent = local.getDiscoveryAgent();
  } catch (BluetoothStateException ex) {
   ex.printStackTrace();
  }
  try {
   agent.startInquiry(DiscoveryAgent.GIAC, this);
  } catch (BluetoothStateException ex) {
   ex.printStackTrace();
  }
 }
 public void pauseApp() {}
 public void destroyApp(boolean unconditional) {}
 public void commandAction(Command c, Displayable d) {
  if (c == Exit) {
   this.destroyApp(true);
   notifyDestroyed();
  }

  if (c == Refresh) {
   this.startApp();
  }
 }
 public void deviceDiscovered(RemoteDevice btDevice, DeviceClass cod) {
  String deviceaddress = null;
  try {
   deviceaddress = btDevice.getBluetoothAddress(); //btDevice.getFriendlyName(true);
  } catch (Exception ex) {
   ex.printStackTrace();
  }
  deviceList.insert(0, deviceaddress, null);
 }
 public void servicesDiscovered(int transID, ServiceRecord[] servRecord) {
  throw new UnsupportedOperationException( & quot; Not supported yet. & quot;);
 }
 public void serviceSearchCompleted(int transID, int respCode) {
  throw new UnsupportedOperationException( & quot; Not supported yet. & quot;);
 }
 public void inquiryCompleted(int discType) {
  Alert dialog = null;
  if (discType != DiscoveryListener.INQUIRY_COMPLETED) {
   dialog = new Alert( & quot; Bluetooth Error & quot;, & quot; The inquiry failed to complete normally & quot;, null,
    AlertType.ERROR);
  } else {
   dialog = new Alert( & quot; Inquiry Completed & quot;, & quot; The inquiry completed normally & quot;,
    null, AlertType.INFO);
  }
  dialog.setTimeout(500);
  Display.getDisplay(this).setCurrent(dialog);
 }
}
''')
	
def print4():
	print('deffie  \n')
	print('''
def exprcal(a, b, p):
    return ((a**b)%p)

def encr(s, key):
		result = ""
		for c in s:
			if(c.isupper()):
				result += chr((ord(c) + key-65) % 26 + 65)
			else:
				result += chr((ord(c) + key-97) % 26 + 97)
		return result

if __name__ == "__main__":
		P = int(input("Value of Public key for Alice: "))
		G = int(input("Value of Public key for Bob: "))
		a = int(input("Private key of Alice: "))
		x = exprcal(G, a, P) #9^4 mod 23
		b = int(input("Private key of Bob: "))
		y = exprcal(G, b, P) #9^3 mod 23
		Ka = exprcal(y, a, P)
		Kb = exprcal(x, b, P)
		print("Secret key for Alice = ", Ka)
		print("Secret key for Alice = ", Kb)
		
		s = input("Enter string to encrypt: ")
		print(encr(s, Ka))

    # 23 9 4 3 9 9 ABcd
''')

def print5():
	print('rsa \n')
	print('''p = int(input("Enter the value of p (prime number)"))
q = int(input("Enter the value of q (prime number)"))

n = p * q
print("Value of n is: ",n)

totient = (p-1)*(q-1)
print("Value of totient is: ",totient)

for i in range(2,totient):
		if(totient%i!=0):
			e=i
			break

print("Value of e is: ",e)
		
d = (e**-1)% totient
 
plain_text = int(input("Enter plain text: ")) 
cypher_text = (plain_text ** e) % n
print("Cipher text is: ",cypher_text)
 
plain_text2 = (cypher_text ** d) % n
print("Claculated plain text is: ",int(plain_text2))

#5 7 2	
''')
def print6():
	print('ns2-hidden \n')
	print('''
#Create a simulator object
set ns [new Simulator]

#Define different colors for data flows
$ns color 1 Blue
$ns color 2 Red

#Open the nam trace file
set nf [open out.nam w]
$ns namtrace-all $nf

#Define a 'finish' procedure
proc finish {} {
        global ns nf
        $ns flush-trace
	#Close the trace file
        close $nf
	#Execute nam on the trace file
        exec nam out.nam &
        exit 0
}

#Create four nodes
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]

#Create links between the nodes
$ns duplex-link $n0 $n2 1Mb 10ms DropTail
$ns duplex-link $n1 $n2 1Mb 10ms DropTail
$ns duplex-link $n3 $n2 1Mb 10ms DropTail


$ns duplex-link-op $n0 $n2 orient right-down
$ns duplex-link-op $n1 $n2 orient right-up
$ns duplex-link-op $n2 $n3 orient right

#Monitor the queue for the link between node 2 and node 3
#set aa [$ns duplex-link-op $n2 $n3 queuePos 0.5]
#puts $aa

$ns duplex-link-op $n2 $n3 queuePos 0.5

$ns queue-limit $n2 $n3 10


#Create a UDP agent and attach it to node n0
set udp0 [new Agent/UDP]
$udp0 set class_ 1
$ns attach-agent $n0 $udp0

# Create a CBR traffic source and attach it to udp0
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 500
$cbr0 set interval_ 0.005
$cbr0 attach-agent $udp0

#Create a UDP agent and attach it to node n1
set udp1 [new Agent/UDP]
$udp1 set class_ 2
$ns attach-agent $n1 $udp1

# Create a CBR traffic source and attach it to udp1
set cbr1 [new Application/Traffic/CBR]
$cbr1 set packetSize_ 500
$cbr1 set interval_ 0.005
$cbr1 attach-agent $udp1

#Create a Null agent (a traffic sink) and attach it to node n3
set null0 [new Agent/Null]
$ns attach-agent $n3 $null0

#Connect the traffic sources with the traffic sink
$ns connect $udp0 $null0  
$ns connect $udp1 $null0

#Schedule events for the CBR agents
$ns at 0.5 "$cbr0 start"
$ns at 1.0 "$cbr1 start"
$ns at 4.0 "$cbr1 stop"
$ns at 4.5 "$cbr0 stop"


#Call the finish procedure after 5 seconds of simulation time
$ns at 5.0 "finish"

#Run the simulation
$ns run

''')
