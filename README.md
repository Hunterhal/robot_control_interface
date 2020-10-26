This python qt based interface transmits joystick commands through socket (UDP) communication.  
Main algorithm works on qt timer with 50 millisecond intervals.  
The packet that is send constructed with start "!JOY" and stop bytes "*", every data is seperated with ",", and each packet length is 100 bytes.   

Example packet is shown below  
!JOY,-0.01,-0.01,-1.00,+0.00,0,0,0,0,0,0,0,0,0,0,0,0,(0, 0),****************************************  

Requirements
Python 
Qt5
Pygame
Socket