This python qt based interface transmits joystick commands through socket (UDP) communication.  
Main algorithm works on qt timer with 50 millisecond intervals.  
The packet that is send constructed with start "!JOY" and stop bytes "*", every data is seperated with ",", and each packet length is 100 bytes.   

The maximum packet size and interval can be changed through the python script

Example packet is shown below  
!JOY,-0.01,-0.01,-1.00,+0.00,0,0,0,0,0,0,0,0,0,0,0,0,0,0,****************************************  

This packet can be processed by splitting or parsing the data ","

Requirements  
Python   
Qt5  
Pygame  
Socket  

For pyqt user interface qt designer can be used the .ui file can be converted using "pyuic5 untitled.ui -o user_interface.py"  

For any other environment just change the UDP IP and Port
On the receiver device, which can be Nvidia Jetson Tx1, Nano, ..., Raspberry Pi, PC, NodeMCU, or any other device supports UDP (Prefreably over Wi-Fi), connect to same network and enter the IP and Port of the device

To - Do list add 
WebSocket and TCP/IP 