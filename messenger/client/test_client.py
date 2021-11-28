import socket
import pickle
from messenger.common.constants import SERVER, PORT, FORMAT, HEADER_SIZE
from messenger.common.communication import Request, Mess, LogIn
from messenger.common.constants import RequestType


class TestClient:
    def __init__(self):
        self.tcp_client = None
        # self.udp_client = ? For audio and video chats

    def start(self):
        address = (SERVER, PORT)
        print("[INFO:CLIENT] Starting client app...")
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[INFO:CLIENT] Connecting to server...")
        self.tcp_client.connect(address)

    def send_request(self, req_type, content):
        req = Request(req_type, content)
        pickled_req = pickle.dumps(req)
        pickled_req_len = len(pickled_req)
        header = str(pickled_req_len).encode(FORMAT)
        header += b' ' * (HEADER_SIZE - len(header))
        self.tcp_client.send(header)
        self.tcp_client.send(pickled_req)
############# BASE ABOVE

    def send_LOGIN_request(self):
        self.send_request(RequestType.LOG_IN, LogIn("client@gmail.com", "super-tajne-hasło"))
