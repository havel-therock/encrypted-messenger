import socket
import hashlib
import pickle
import threading
import time
from pathlib import Path
from messenger.common.constants import SERVER, PORT, FORMAT, HEADER_SIZE
from messenger.common.communication import Request, Mess, LogIn
from messenger.common.constants import RequestType


class Client:
    loggedInFlag = False
    msgDatabase= list()
    connected = True

    def __init__(self):
        self.tcp_client = None
        # self.udp_client = ? For audio and video chats

    def start(self):

        address = (SERVER, PORT)
        #daniel wczytanie bazy do msgDatabase i wypisanie jej na ekran
        print("[INFO:CLIENT] Starting client app...")
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[INFO:CLIENT] Connecting to server...")
        self.tcp_client.connect(address)

        thread = threading.Thread(target=self.client_receiver, args=(self.tcp_client, self.loggedInFlag))
        thread.start()

        while not self.loggedInFlag:
            print("Enter your nickname")
            nickname = input()
            print("Enter your password")
            password = input()
            self.send_request(RequestType.LOG_IN, LogIn(nickname, password))

            #do wywalenia
            self.loggedInFlag = True
            self.connected = True

            wait_iterator = 0
            while not self.loggedInFlag and wait_iterator < 10:
                time.sleep(0.5)
                wait_iterator += 1

            if wait_iterator >= 10:
                print("server unreachable or wrong login data")

        # after log_in
        print("[INFO:CLIENT] After log_in...")

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
                self.connected = False
            else:
                m = Mess(nickname, receiver, "hash", msg)
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
        while self.connected:
            msg_length = conn.recv(HEADER_SIZE).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                pickled_msg = conn.recv(msg_length)  # is it possible to stuck here if no message was sent after sending the header
                self.handle_action(pickled_msg)

    def handle_action(self, pickled_server_request):
        server_request = pickle.loads(pickled_server_request)
        # dev note: python 3.10 has switch statements... older versions doesn't
        req = server_request.request_type

        if req == RequestType.LOG_IN:
            a = server_request.content.email
            b = server_request.content.passwd
            if a == "OK":
                self.loggedInFlag = True
        elif req == RequestType.SEND_MSG:
            #display message and add to database
            #daniel
            print(req.content)
            self.msgDatabase.append(req.content)
            pass

    ############# BASE ABOVE

    def send_LOGIN_request(self):
        self.send_request(RequestType.LOG_IN, LogIn("client@gmail.com", "super-tajne-hasło"))
