import pygame
import time
import sys 
import socket

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QListWidget, QGridLayout, QLabel, QLineEdit, QRadioButton
from PyQt5.QtCore import QTimer, QDateTime

from user_interface import Ui_Dialog

class WinForm(QWidget):
    def __init__(self, parent=None):
        super(WinForm, self).__init__(parent)
        self.setWindowTitle("Robot Control Interface")

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.checkBtns = []
        self.checkBtns.append(self.ui.checkBtn_1)
        self.checkBtns.append(self.ui.checkBtn_2)
        self.checkBtns.append(self.ui.checkBtn_3)
        self.checkBtns.append(self.ui.checkBtn_4)
        self.checkBtns.append(self.ui.checkBtn_5)
        self.checkBtns.append(self.ui.checkBtn_6)
        self.checkBtns.append(self.ui.checkBtn_7)
        self.checkBtns.append(self.ui.checkBtn_8)
        self.checkBtns.append(self.ui.checkBtn_9)
        self.checkBtns.append(self.ui.checkBtn_10)
        self.checkBtns.append(self.ui.checkBtn_11)
        self.checkBtns.append(self.ui.checkBtn_12)

        self.timer=QTimer()
        self.timer.timeout.connect(self.showTime)

        self.ui.pushBtnStart.clicked.connect(self.startTimer)
        self.ui.pushBtnStop.clicked.connect(self.endTimer)

        #Intialize Joystick
        pygame.display.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def showTime(self):
        # Get next pygame event
        pygame.event.pump()
        send_string = "!JOY,"

        xAxis = self.controller.get_axis(1)
        send_string += '%+2.2f,' % xAxis
        self.ui.textXAxis.setText('%+2.2f' % xAxis)

        yAxis = self.controller.get_axis(0)
        send_string += '%+2.2f,' % yAxis
        self.ui.textYAxis.setText('%+2.2f' % yAxis)

        zAxis = self.controller.get_axis(2)
        send_string += '%+2.2f,' % zAxis
        self.ui.textZAxis.setText('%+2.2f' % zAxis)

        zRot = self.controller.get_axis(3)
        send_string += '%+2.2f,' % zRot
        self.ui.textZRot.setText('%+2.2f' % zRot)

        for k in range(self.controller.get_numbuttons()):
            send_string += '%d,' % self.controller.get_button(k)
            self.checkBtns[k].setChecked(bool(self.controller.get_button(k)))
        for k in range(self.controller.get_numhats()):
            pov = self.controller.get_hat(k)
            pov_str = str(pov[0]) + "," + str(pov[1]) 
            self.ui.textPov.setText(pov_str)
            send_string += pov_str + ","

        self.ui.textPacket.setText(send_string)

        send_string += "*"
        while len(send_string) != 100:
            send_string += "*"
        
        self.sock.sendto(str.encode(send_string), (self.UDP_IP, self.UDP_PORT))

    def startTimer(self):
        #Initialize UDP Socket
        self.UDP_IP = self.ui.textIP.text()
        self.UDP_PORT = int(self.ui.textPort.text())
        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

        self.timer.start(50)
        self.ui.pushBtnStart.setEnabled(False)
        self.ui.pushBtnStop.setEnabled(True)

    def endTimer(self):
        self.timer.stop()
        self.ui.pushBtnStart.setEnabled(True)
        self.ui.pushBtnStop.setEnabled(False)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    form=WinForm()
    form.show()
    sys.exit(app.exec_())