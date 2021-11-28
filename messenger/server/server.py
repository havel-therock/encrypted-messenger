import socket
import threading
import hashlib
import pickle
from messenger.common.constants import RequestType


class Server:

    # active_IPs = []
    active_users = list()

    def __init__(self, **kwargs):
        # self.active_users = {} # user_id : ip_address : last seen time
        self.header_size = 64
        self.format = "utf-8"
        # this sometimes return loopback ip addres instead of just private network ip. 127... instead of 196
        # to work this from internet, check for a public IP and put it here
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.port = 6667
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

        #  socket.setdefaulttimeout(None)  <-- default value

        # socket.settimeout(0.0001)
        while self.server_running:

            conn, ip_addr = server.accept()
            #print(conn)
            #print(ip_addr)
            #  if conn is not None and ip_addr is not None:
            thread = threading.Thread(target=self.handle_client, args=(conn, ip_addr))
            thread.start()
            print(f"[INFO] ACTIVE CONNECTIONS: {threading.active_count() - 1}")
                # conn = None
                # ip_addr = None

    def shut_down(self):
        # clean_up all clients....
        # disconnect them close connection to data base ensure every process that is running is stopped properly
        self.server_running = False

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

    def handle_client(self, conn, ip_addr):
        print(f"[INFO] {ip_addr} connected.")
        connected = True
        while connected:
            msg_length = conn.recv(self.header_size).decode(self.format)
            if msg_length:
                msg_length = int(msg_length)
                pickled_msg = conn.recv(msg_length)  # is it possible to stuck here if no message was sent after sending the header
                self.handle_action(pickled_msg, ip_addr,conn)
            #connected = self.check_connection(ip_addr)
        #self.remove_user(ip_addr)
        conn.close()

    def handle_action(self, pickled_client_request, ip_addr, conn):
        client_request = pickle.loads(pickled_client_request)
        # dev note: python 3.10 has switch statements... older versions doesn't
        req = client_request.request_type
        ####
        print(client_request.request_type)
        print(client_request.content)
        ####
        #if req == RequestType.LOG_IN:
        #    self.action_login(client_request, ip_addr, conn)
        #el
        if req == RequestType.DISCONNECT:
            self.action_disconnect(ip_addr)
        #else:  # if clients talk non-existing requests -> disconnect them
        #    self.action_disconnect(ip_addr)

    def action_login(self, client_request, ip_addr, conn):
        user = self.get_clients_by_ip(ip_addr)
        if user is not None:
            user.conn_status = "active"
        else:
            pass #.log_in()

    def action_sync(self):
        pass

    def action_send_message(self):
        pass

    def action_disconnect(self, ip_addr):
        for user in self.active_users:
            if user.ip_address == ip_addr:
                user.conn_status = "disconnected"  # potential locking needed for thread safe. Right now not needed
                return
        self.active_users.append(User(None, None, ip_addr, None, conn_status="disconnected"))

# figure out method for detecting disconnected clients which has not log out properly by sending DISCONNECT_MESSAGE
# probably ping  every 5 minutes all inactive user if they are online... If no response... remove them from active users list and kill their thread


# move class to another module?
class User:
    def __init__(self, user_id, comm_socket, ip_address, last_seen, **kwargs):
        self.user_id = user_id
        self.communication_socket = comm_socket
        self.ip_address = ip_address
        self.last_seen = last_seen
        self.conn_status = "active"  # active|disconnected
        if "conn_status" in kwargs:
            self.conn_status = kwargs["conn_status"]
