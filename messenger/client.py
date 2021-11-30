#!/usr/bin/env python3

import socket
import hashlib
import pickle
import threading
import time
import clientDBHandler
from pathlib import Path
from common.constants import SERVER, PORT, FORMAT, HEADER_SIZE
from common.communication import Request, Mess, LogIn
from common.constants import RequestType


class Client:
    loggedInFlag = False
    msgDatabase= list()
    receiverON = True

    def __init__(self):
        self.tcp_client = None
        clientDBHandler.setup_database()
        print("a")
        # self.udp_client = ? For audio and video chats

    def start(self):
        address = (SERVER, PORT)

        print("[INFO:CLIENT] Starting client app...")
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[INFO:CLIENT] Connecting to server...")
        self.tcp_client.connect(address)

        self.receiverON = True
        thread = threading.Thread(target=self.client_receiver, args=(self.tcp_client, self.loggedInFlag))
        thread.start()

        while not self.loggedInFlag:
            print("Enter your nickname")
            self.nickname = input()
            print("Enter your password")
            password = input()
            self.send_request(RequestType.LOG_IN, LogIn(self.nickname, password))


            wait_iterator = 0
            while not self.loggedInFlag and wait_iterator < 10:
                time.sleep(0.5)
                wait_iterator += 1

            if wait_iterator >= 10:
                print("server unreachable or wrong login data")
                #gui pop

        # after log_in
        print("[INFO:CLIENT] After log_in...")
        # daniel wczytanie bazy do msgDatabase i wypisanie jej na ekran
        tmp = clientDBHandler.get_all_data()
        for msg in tmp:
            self.msgDatabase.append(msg)

        while self.loggedInFlag:
            print("Enter receiver")
            receiver = input()
            print("Enter your message")
            msg = input()

            if receiver == "DISCONNECT" or msg == "DISCONNECT":
                m = Mess("", "", "", "")
                self.send_request(RequestType.DISCONNECT, m)
                self.tcp_client.close()
                self.loggedInFlag = False
                self.receiverON = False
            else:
                m = Mess(self.nickname, receiver, "hash", msg)
                self.send_request(RequestType.SEND_MSG, m)

        print("[INFO:CLIENT] Correctly disconnected")

    def send_request(self, req_type, content):
        req = Request(req_type, content)
        pickled_req = pickle.dumps(req)
        pickled_req_len = len(pickled_req)
        header = str(pickled_req_len).encode(FORMAT)
        header += b' ' * (HEADER_SIZE - len(header))
        self.tcp_client.send(header)
        self.tcp_client.send(pickled_req)

    def client_receiver(self, conn,n):
        print(f"[RECEIVER INFO] receiver starting.")
        while self.receiverON:
            msg_length = conn.recv(HEADER_SIZE).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                pickled_msg = conn.recv(msg_length)  # is it possible to stuck here if no message was sent after sending the header
                self.handle_action(pickled_msg)

    def handle_action(self, pickled_server_request):
        server_request = pickle.loads(pickled_server_request)
        # dev note: python 3.10 has switch statements... older versions doesn't
        req = server_request.request_type

        if req == RequestType.LOG_IN__OK:
            self.loggedInFlag = True
        elif req == RequestType.USERNAME_TAKEN:
            print("ERROR: USERNAME_TAKEN")
        elif req == RequestType.NEW_MESSAGE:
            #display message and add to database
            #print(server_request.content)
            self.print_msg(server_request.content.msg_sender,
                           self.nickname,
                           server_request.content.message)
            #daniel save to database
            clientDBHandler.save_message(server_request.content.msg_sender,
                                         server_request.content.msg_sender,
                                         round(time.time() * 1000),
                                         server_request.content.message)
            self.msgDatabase.append(server_request.content)
        else:
            print("unknown request type")

    def print_msg(self,sender,receiver,msg):
        text = "({} -> {}): {}".format(sender,receiver,msg)

    def send_LOGIN_request(self):
        self.send_request(RequestType.LOG_IN, LogIn("client@gmail.com", "super-tajne-hasło"))

if __name__ == "__main__":
    client = Client()
    client.start()
    #  client.send_LOGIN_request()
