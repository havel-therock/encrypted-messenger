#!/usr/bin/env python3

import sys,time
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QScrollBar,QSplitter,QTableWidgetItem,QTableWidget,QComboBox,QVBoxLayout,QGridLayout,QDialog,QWidget, QPushButton, QApplication, QMainWindow,QAction,QMessageBox,QLabel,QTextEdit,QProgressBar,QLineEdit
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
            self.dupsko(tmp[0], tmp[1])
            self.chatTextField.setText("")
        
    def dupsko(self,auth,msg):
        text=auth + " > " + msg
        font=self.chat.font()
        font.setPointSize(13)
        self.chat.setFont(font)
        textFormatted='{:<80}'.format(text)
        self.chat.append(textFormatted)

    def handle_action(self, pickled_server_request):
        server_request = pickle.loads(pickled_server_request)
        # dev note: python 3.10 has switch statements... older versions doesn't
        req = server_request.request_type

        if req == RequestType.LOG_IN:
            a = server_request.content.email
            b = server_request.content.passwd
            self.dupsko(a, b)
            if a == "OK":
                self.loggedInFlag = True
        elif req == RequestType.SEND_MSG:
            #display message and add to database
            #daniel
            dupsko(req.content.msg_sender, req.content.message)
            self.msgDatabase.append(req.content)
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window.start()
    sys.exit(app.exec_())
