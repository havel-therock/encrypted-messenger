#!/usr/bin/env python3

import sys,time
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QInputDialog ,QScrollBar,QSplitter,QTableWidgetItem,QTableWidget,QComboBox,QVBoxLayout,QGridLayout,QDialog,QWidget, QPushButton, QApplication, QMainWindow,QAction,QMessageBox,QLabel,QTextEdit,QProgressBar,QLineEdit
from PyQt5.QtCore import QCoreApplication
import socket
from threading import Thread 
from socketserver import ThreadingMixIn 
from client import *

import socket
import hashlib
import pickle
import threading
import time
from pathlib import Path
from common.constants import SERVER, PORT, FORMAT, HEADER_SIZE
from common.communication import Request, Mess, LogIn
from common.constants import RequestType

tcpClientA=None

class Window(QWidget, Client):
    def __init__(self):
        super().__init__()
        self.chatTextField=QLineEdit(self)
        self.chatTextField.resize(480,100)
        self.chatTextField.move(10,350)
        
        self.btnSend=QPushButton("Send",self)
        self.btnSend.resize(480,30)
        self.btnSendFont=self.btnSend.font()
        self.btnSendFont.setPointSize(15)
        self.btnSend.setFont(self.btnSendFont)
        self.btnSend.move(10,460)
        self.btnSend.setStyleSheet("background-color: #F7CE16")
        self.btnSend.clicked.connect(self.send)

        self.chatBody=QVBoxLayout(self)
        # self.chatBody.addWidget(self.chatTextField)
        # self.chatBody.addWidget(self.btnSend)
        # self.chatWidget.setLayout(self.chatBody)
        splitter=QSplitter(QtCore.Qt.Vertical)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        splitter.addWidget(self.chat)
        splitter.addWidget(self.chatTextField)
        splitter.setSizes([400,100])

        splitter2=QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.addWidget(self.btnSend)
        splitter2.setSizes([200,10])

        self.chatBody.addWidget(splitter2)


        self.setWindowTitle("Chat Application")
        self.resize(500, 500)

    def send(self):
        text=self.chatTextField.text()
        tmp = text.split(maxsplit=1)
        if len(tmp)>1:
            self.print_msg(self.nickname, tmp[0], tmp[1])
            m = Mess(self.nickname, tmp[0], "hash", tmp[1])
            self.send_request(RequestType.SEND_MSG, m)
            self.chatTextField.setText("")
            clientDBHandler.save_message(self.nickname,
                                         self.nickname,
                                         tmp[0],
                                         round(time.time() * 1000),
                                         tmp[1])
        
    def print_msg(self,sender,receiver,msg):
        text = "[{} -> {}] {}".format(sender,receiver,msg)
        font=self.chat.font()
        font.setPointSize(13)
        self.chat.setFont(font)
        textFormatted='{:<80}'.format(text)
        self.chat.append(textFormatted)

    def closeEvent(self, event):
        print("close x")
        m = Mess("", "", "", "")
        self.send_request(RequestType.DISCONNECT, m)
        self.tcp_client.close()
        self.loggedInFlag = False
        self.receiverON = False

    def gettext(self, t):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', t)
        if ok:
            return text


    def startGUI(self):
        address = (SERVER, PORT)

        print("[INFO:CLIENT] Starting client app...")
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[INFO:CLIENT] Connecting to server...")
        self.tcp_client.connect(address)

        self.receiverON = True
        thread = threading.Thread(target=self.client_receiver, args=(self.tcp_client, self.loggedInFlag))
        thread.start()

        while not self.loggedInFlag:
            #print("Enter your nickname")
            #self.nickname = input()
            #print("Enter your password")
            #password = input()

            self.nickname = ""
            self.password = ""



            while self.nickname == "" or  self.password == "":
                self.nickname=self.gettext("Enter your nickname")
                self.password = self.gettext("Enter your password")


            self.send_request(RequestType.LOG_IN, LogIn(self.nickname, self.password))

            wait_iterator = 0
            while not self.loggedInFlag and wait_iterator < 10:
                time.sleep(0.5)
                wait_iterator += 1

            if wait_iterator >= 10:
                print("server unreachable or wrong login data")
                # gui pop

        # after log_in
        print("[INFO:CLIENT] After log_in...")

        # daniel wczytanie bazy do msgDatabase i wypisanie jej na ekran
        tmp = clientDBHandler.get_all_data()
        for msg in tmp:
            self.msgDatabase.append(msg)
#            print(msg)
            if self.nickname in msg[1:3]:
                self.print_msg(msg[1],msg[2],msg[4])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window.startGUI()
    sys.exit(app.exec_())
