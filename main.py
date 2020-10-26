import pygame
import time
import sys 
import socket

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QListWidget, QGridLayout, QLabel, QLineEdit
from PyQt5.QtCore import QTimer, QDateTime

class WinForm(QWidget):
    def __init__(self, parent=None):
        super(WinForm, self).__init__(parent)
        self.setWindowTitle("Robot Control Interface")

        self.setFixedWidth(400)
        self.setFixedHeight(400)

        self.listFile=QListWidget()
        self.label=QLabel('Label')

        self.labelXAxis=QLabel('XAxis:')
        self.textXAxis = QLineEdit(self)
        self.labelYAxis=QLabel('YAxis:')
        self.textYAxis = QLineEdit(self)
        self.labelZRot=QLabel('ZRot:')
        self.textZRot = QLineEdit(self)
        self.labelZAxis=QLabel('ZAxis:')
        self.textZAxis = QLineEdit(self)

        self.startBtn=QPushButton('Start')
        self.endBtn=QPushButton('Stop')

        layout=QGridLayout()
        layout.addWidget(self.label,0,0,1,2)
        layout.addWidget(self.startBtn,1,0)
        layout.addWidget(self.endBtn,1,1)

        layout.addWidget(self.labelXAxis,2,0)
        layout.addWidget(self.textXAxis,2,1)
        layout.addWidget(self.labelYAxis,3,0)
        layout.addWidget(self.textYAxis,3,1)
        layout.addWidget(self.labelZRot,4,0)
        layout.addWidget(self.textZRot,4,1)
        layout.addWidget(self.labelZAxis,5,0)
        layout.addWidget(self.textZAxis,5,1)

        self.timer=QTimer()
        self.timer.timeout.connect(self.showTime)

        self.startBtn.clicked.connect(self.startTimer)
        self.endBtn.clicked.connect(self.endTimer)

        #Initialize UDP Socket
        self.UDP_IP = "192.168.0.101"
        self.UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

        #Intialize Joystick
        pygame.display.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        self.setLayout(layout)

    def showTime(self):
        # Get next pygame event
        pygame.event.pump()
        send_string = "!JOY,"

        xAxis = self.controller.get_axis(1)
        send_string += '%+2.2f,' % xAxis
        self.textXAxis.setText('%+2.2f,' % xAxis)

        yAxis = self.controller.get_axis(0)
        send_string += '%+2.2f,' % yAxis
        self.textYAxis.setText('%+2.2f,' % yAxis)

        zAxis = self.controller.get_axis(2)
        send_string += '%+2.2f,' % zAxis
        self.textZAxis.setText('%+2.2f,' % zAxis)

        zRot = self.controller.get_axis(3)
        send_string += '%+2.2f,' % zRot
        self.textZRot.setText('%+2.2f,' % zRot)

        for k in range(self.controller.get_numbuttons()):
            send_string += '%d,' % self.controller.get_button(k)
        for k in range(self.controller.get_numhats()):
            send_string += str(self.controller.get_hat(k)) + ","

        send_string += "*"
        while len(send_string) != 100:
            send_string += "*"
        
        self.label.setText(send_string)
        self.sock.sendto(str.encode(send_string), (self.UDP_IP, self.UDP_PORT))

    def startTimer(self):
        self.timer.start(50)
        self.startBtn.setEnabled(False)
        self.endBtn.setEnabled(True)

    def endTimer(self):
        self.timer.stop()
        self.startBtn.setEnabled(True)
        self.endBtn.setEnabled(False)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    form=WinForm()
    form.show()
    sys.exit(app.exec_())