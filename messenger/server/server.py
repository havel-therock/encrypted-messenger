#!/usr/bin/env python3

import socket
import threading
import pickle
import time
import urllib.request

from .user import User
from messenger.comm.constants import PORT, HEADER_SIZE, FORMAT
from messenger.comm.req.request import Request, RequestType
from messenger.comm.req.request_content import LogInContent


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
        self.admin_user = None

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
        # prepare for making server reachable from outside
        # external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        # print(external_ip)
        #
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip_address, self.port))
        print("[INFO:SERVER] Starting server...")
        server.listen()
        print(f"[INFO:SERVER] Server is listening on {self.ip_address}")

        # activate commandline for admin
        thread = threading.Thread(target=self.start_admin_commandline)
        thread.start()

        # main server loop
        while self.server_running:
            conn, ip_address = server.accept()
            user = User(conn, ip_address)
            thread = threading.Thread(target=self.handle_client, args=(user, ))
            user.thread = thread
            thread.start()
            print(f"[INFO] ACTIVE CONNECTIONS: {threading.active_count() - 2}.")
        while threading.active_count() > 1:
            print(f"[INFO] ACTIVE CONNECTIONS: {threading.active_count() - 1}.")
            time.sleep(5)
        print("[INFO] All clients disconnected. Server shutdown...")
        self.admin_user.close()
        server.close()

    # very convenient for development, but admin has all power on Server (can call every function)
    def start_admin_commandline(self):
        while self.server_running:
            command = input().split()
            try:
                if command:
                    server_func = getattr(Server, command[0])
                    args = command[1:]
                    server_func(self, *args)
            except AttributeError:
                print(f"{command[0]}() is not a valid function in Server")
            except TypeError:
                print(f"You passed wrong number of arguments in to {command[0]}() function")

# INTERNAL SERVER FUNCTIONS ###
    def shut_down(self):
        self.server_running = False
        self.admin_user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.admin_user.connect((self.ip_address, self.port))
        for user in self.active_users:
            self.notify_client(user, RequestType.SERVER_SHUTDOWN, None)
            user.active = False
            # DATABASE_ON_SHUTDOWN!!!!
            # disconnect them close connection to data base ensure every process that is running is stopped properly

# END OF INTERNAL SERVER FUNCTIONS ###

# SERVER UTILITY FUNCTIONS ### # make them _private?
    def get_clients_by_ip(self, ip_address):
        for user in self.active_users:
            if user.ip_address == ip_address:
                return user
        return None

    def check_connection(self, ip_address):
        for user in self.active_users:
            if user.ip_address == ip_address:
                if user.conn_status == "disconnected":
                    return False
                else:
                    return True
        return True

    def remove_user(self, ip_address):
        for user in self.active_users:
            if user.ip_address == ip_address:
                self.active_users.remove(user)

# END OF SERVER UTILITY FUNCTIONS ###

# USER THREAD FUNCTION ###
    def handle_client(self, user):
        print(f"[INFO] {user.ip_address} connected.")
        self.active_users.append(user)
        conn = user.conn_socket
        user_reachable = True
        disconnect_counter = 0
        while user.active:
            if disconnect_counter > 100:
                self.action_disconnect(user)
            try:
                # for dev-phase timeout small - for production set to 30 sec to not overwhelm server
                conn.settimeout(3)  # timeout for inactive users set here like 300 sec (5min)
                msg_length = conn.recv(self.header_size).decode(self.format)
                if msg_length:
                    msg_length = int(msg_length)
                    pickled_msg = conn.recv(msg_length)
                    self.handle_action(pickled_msg, user)
                    user_reachable = True
                    disconnect_counter = 0
                else:
                    # when pipe is broken on client side,
                    # it is sending continues empty messages to server
                    disconnect_counter += 1

            except socket.timeout:
                if not user_reachable:
                    self.action_disconnect(user)
                else:
                    print(f"[INFO-DEBUG] Check if {user.ip_address} is active.")
                    user_reachable = False
                    self.ping_client(user)
        print(f"[INFO] User: {user.ip_address} has been disconnected.")
        conn.close()

# USER TASK DELEGATING FUNCTION ###
    def handle_action(self, pickled_client_request, user):
        client_request = pickle.loads(pickled_client_request)
        if not isinstance(client_request, Request):
            # action!!! new method <--- not a REQUEST OBJECT  send by client()
            return

        req_type = client_request.request_type
        #### TO delete in future. To comment out when want to use admin console easy
        print(client_request.request_type)
        print(client_request.content)
        ####

        #if req_type == RequestType.LOG_IN:
        #    self.action_login(user, client_request)
        #el
        # dev note: python 3.10 has switch statements... older versions doesn't
        if req_type == RequestType.LOG_IN:  # RequestType.REGISTER: swap to align to tmp client
            if type(client_request.content) is LogInContent:
                self.action_register(user, client_request)
            else:
                self.notify_client(user, RequestType.BAD_REQUEST_CONTENT, None)
        elif req_type == RequestType.PONG:
            # end of checking if user is active. Nothing to be done.
            pass
        elif req_type == RequestType.DISCONNECT:
            self.action_disconnect(user)
        elif user in self.active_users:
            if req_type == RequestType.SEND_MSG:
                self.action_send_message(user, client_request)  # change later to passing only content
            # uncomment in production server, during dev-phase it is useful to not disconnect gibberish clients
            else:  # if clients talk non-existing requests -> disconnect them
                print("user <", user.user_id, "> send nonsense request -->", req_type)
                #  self.action_disconnect(user)
        else:
            print("user <", user.user_id, "> not in active users")
            self.action_disconnect(user)

# CLIENT ACTIONS FUNCTIONS ###
    def action_register(self, user, client_request):
        user.user_id = client_request.content.nickname
        user.user_passwd = client_request.content.passwd
        for usr in self.active_users:
            if usr.user_id == user.user_id and usr is not user:
                print("[INFO] nickname TAKEN")
                self.notify_client(user, RequestType.USERNAME_TAKEN, None)
                return
        self.notify_client(user, RequestType.LOG_IN__OK, None)

    def action_login(self, user):
        print("LogIn")
        #user = self.get_clients_by_ip(ip_address)
        #if user is not None:
        #    user.conn_status = "active"
        #else:
        #    pass #.log_in()

    def action_send_message(self, user, client_request):
        for a_usr in self.active_users:  # later change to search through all rooms id stored in database
            if a_usr.user_id == client_request.content.msg_receiver:
                self.notify_client(a_usr, RequestType.NEW_MESSAGE, client_request.content)
        # when data base included maybe separate server thread for passing messages to clients... observer of rooms?

    def action_disconnect(self, user_to_disconnect):
        if user_to_disconnect in self.active_users:
            self.active_users.remove(user_to_disconnect)
        user_to_disconnect.active = False

# END OF CLIENT ACTIONS FUNCTIONS ###

# MAIN METHOD FOR CONSTRUCTING AND SENDING REQUESTS TO CLIENT ###
    @staticmethod
    def notify_client(user, req_type, req_data):
        req = Request(req_type, req_data)
        pickled_req = pickle.dumps(req)
        pickled_req_len = len(pickled_req)
        header = str(pickled_req_len).encode(FORMAT)
        header += b' ' * (HEADER_SIZE - len(header))
        user.conn_socket.send(header)
        user.conn_socket.send(pickled_req)

# SPECIFIC REQUESTS TO CLIENT

    def ping_client(self, user):
        self.notify_client(user, RequestType.PING, None)

# END OF SPECIFIC REQUESTS TO CLIENT

# SERVER REQUESTS TO DATABASE

# END SERVER REQUESTS TO DATABASE


# SERVER TYPE OF ACCTIONS:
# 0. Internal work              functions server_*
# 1. Hearing from clients       functions cli_action_* (work triggered by client request)
# 2. Notifing client            functions cli_request_*
# 3. Pushing to database        functions db_request_*
# 4. Getting from database      functions db_action_*
# hearing jobs and delegating to proper actions/requests           functions (server_)handle_client_/_db_*
