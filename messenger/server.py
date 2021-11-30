#!/usr/bin/env python3

import socket
import threading
import hashlib
import pickle
from common.constants import RequestType, PORT, HEADER_SIZE, FORMAT
from common.communication import Request

class Server:

    # active_IPs = []
    active_users = list()

    def __init__(self, **kwargs):
        # self.active_users = {} # user_id : ip_address : last seen time
        self.header_size = HEADER_SIZE
        self.format = FORMAT
        # this sometimes return loopback ip addres instead of just private network ip. 127... instead of 196
        # to work this from internet, check for a public IP and put it here
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.port = PORT
        self.server_running = True

        if "header_size" in kwargs:
            self.header_size = kwargs["header_size"]
        if "format" in kwargs:
            self.format = kwargs["format"]
        if "ip_address" in kwargs:
            self.ip_address = kwargs["ip_address"]
        if "port" in kwargs:
            self.port = kwargs["port"]
        if "header_size" in kwargs:
            self.header_size = kwargs["header_size"]

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip_address, self.port))
        print("[INFO:SERVER] Starting server...")
        server.listen()
        print(f"[INFO:SERVER] Server is listening on {self.ip_address}")
        while self.server_running:
            conn, ip_addr = server.accept()
            user = User(None, conn, ip_addr)
            thread = threading.Thread(target=self.handle_client, args=(user, ))
            user.thread = thread
            thread.start()
            print(f"[INFO] ACTIVE CONNECTIONS: {threading.active_count() - 1}")
        socket.close()

    def shut_down(self):
        # TO DO
        # clean_up all clients.... maybe send the message server is going to sleep...
        # disconnect them close connection to data base ensure every process that is running is stopped properly
        self.server_running = False
        #connect closing dummy client for passing socket.accept() stuck

    def get_clients_by_ip(self, ip_addr):
        for user in self.active_users:
            if user.ip_address == ip_addr:
                return user
        return None

    def check_connection(self, ip_addr):
        for user in self.active_users:
            if user.ip_address == ip_addr:
                if user.conn_status == "disconnected":
                    return False
                else:
                    return True
        return True

    def remove_user(self, ip_addr):
        for user in self.active_users:
            if user.ip_address == ip_addr:
                self.active_users.remove(user)

    def handle_client(self, user):
        print(f"[INFO] {user.ip_addr} connected.")
        conn = user.conn_socket
        ip_addr = user.ip_addr
        connected = True
        # to debug clients that are closed by sigkill and before timeout is reached...
        # why they are not cleared?
        while connected:
            try:
                conn.settimeout(300) # timeout for inactive users set here like 300 sec (5min)
                msg_length = conn.recv(self.header_size).decode(self.format)
                conn.settimeout(None)
            except socket.timeout:
                print(ip_addr, " timeouted")
                msg_length = ""
                self.action_disconnect(user)  # replace later with ping check - If client not respond in 30 seconds disconnect them
            if msg_length:
                msg_length = int(msg_length)
                try:
                    conn.settimeout(60)  # in production extend to 60 sec
                    pickled_msg = conn.recv(msg_length)
                    conn.settimeout(None)
                    self.handle_action(pickled_msg, user)
                except socket.timeout:
                    print(ip_addr, " timeouted second place")
                    # user hung... sent HEADER but not DATA... disconnect this user
                    self.action_disconnect(user)
            if user.conn_status == "disconnect":
                connected = False
        if user in self.active_users:
            self.active_users.remove(user)
        conn.close()

    def handle_action(self, pickled_client_request, user):
        client_request = pickle.loads(pickled_client_request)
        # dev note: python 3.10 has switch statements... older versions doesn't
        req_type = client_request.request_type
        ####
        print(client_request.request_type)
        print(client_request.content)
        ####
        #if req_type == RequestType.LOG_IN:
        #    self.action_login(user, client_request)
        #el
        if req_type == RequestType.LOG_IN:  # RequestType.REGISTER: swap to aligin to tmp client
            self.action_register(user, client_request)
        elif req_type == RequestType.DISCONNECT:
            self.action_disconnect(user)
        elif user in self.active_users:
            if req_type == RequestType.SEND_MSG:
                self.action_send_message(user, client_request) # change later to passing only content
            # uncomment in production server, during dev-phase it is useful to not disconnect gibberish clients
            else:  # if clients talk non-existing requests -> disconnect them
                print("user <", user.user_id, "> send nonsense request -->", req_type)
                #self.action_disconnect(user)
        else:
            print("user <", user.user_id, "> not in active users")
            self.action_disconnect(user)

    def action_register(self, user, client_request):
        user.user_id = client_request.content.nickname
        user.user_passwd = client_request.content.passwd
        for usr in self.active_users:
            if usr.user_id == user.user_id:
                print("[INFO] nickname TAKEN")
                self.notify_client(user, RequestType.USERNAME_TAKEN, None)
                return
        self.active_users.append(user)
        self.notify_client(user, RequestType.LOG_IN__OK, None)

    def action_login(self, user):
        print("LogIn")
        #user = self.get_clients_by_ip(ip_addr)
        #if user is not None:
        #    user.conn_status = "active"
        #else:
        #    pass #.log_in()

    def action_send_message(self, user, client_request):
        for a_usr in self.active_users:  # later change to search through all rooms id stored in database
            if a_usr.user_id == client_request.content.msg_reciver:
                self.notify_client(a_usr, RequestType.NEW_MESSAGE, client_request.content)
        # when data base included maybe separate server thread for passing messages to clients... observer of rooms?

    def action_disconnect(self, user_to_disconnect):
        if user_to_disconnect in self.active_users:
            self.active_users.remove(user_to_disconnect)
        user_to_disconnect.conn_status = "disconnect"

    @staticmethod
    def notify_client(user, req_type, req_data):
        req = Request(req_type, req_data)
        pickled_req = pickle.dumps(req)
        pickled_req_len = len(pickled_req)
        header = str(pickled_req_len).encode(FORMAT)
        header += b' ' * (HEADER_SIZE - len(header))
        user.conn_socket.send(header)
        user.conn_socket.send(pickled_req)

# figure out method for detecting disconnected clients which has not log out properly by sending DISCONNECT_MESSAGE
# probably ping  every 5 minutes all inactive user if they are online... If no response... remove them from active users list and kill their thread


# move class to another module?
class User:
    def __init__(self, user_id, connection_socket, ip_addr, **kwargs):
        self.user_id = user_id
        self.user_passwd = ""
        self.conn_socket = connection_socket
        self.ip_addr = ip_addr
        self.conn_status = "active"  # active|disconnected
        self.thread = None
        if "conn_status" in kwargs:
            self.conn_status = kwargs["conn_status"]

if __name__ == "__main__":
    # Starting server
    server = Server()
    server.start()
