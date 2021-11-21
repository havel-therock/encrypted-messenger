import socket
import hashlib
import pickle
import threading
import time


class Mess:
    def __init__(self, msg_sender, msg_receiver, msg_hash, message):
        self.msg_sender = msg_sender
        self.msg_receiver = msg_receiver
        self.msg_hash = msg_hash
        self.message = message


HEADER_SIZE = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECTED_MESSAGE = "###DISCONNECTED###"
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)

server_response_flag = True


def send_hello():
    receiver = "server-hello"
    global server_response_flag
    server_response_flag = False
    m1 = Mess(nickname, receiver, "", "hello server my name is " + nickname)
    m1Pickle = pickle.dumps(m1)
    client.send(m1Pickle)

    wait_iterator = 0
    while not server_response_flag or wait_iterator > 10:
        time.sleep(0.5)
        wait_iterator += 1

    if wait_iterator > 10:
        print("server unreachable (hello)")


    # rec = client.recv(4096)  # magic number
    # msg_back = pickle.loads(rec)
    # print("Message-received: {", msg_back.msg_sender, ",", msg_back.msg_receiver,
    #      ",", msg_back.msg_hash, ",", msg_back.message, "}")


def client_receiver():
    global server_response_flag
    while True:
        rec = client.recv(4096)  # magic number
        msg = pickle.loads(rec)
        print("Message-received: {", msg.msg_sender, ",", msg.msg_receiver,
              ",", msg.msg_hash, ",", msg.message, "}")
        if msg.message == "OK" and ( msg.msg_sender == "server-authentication" or msg.msg_sender == "server-hello-authentication"):
            server_response_flag = True
        else:
            localHash = hashlib.sha256(msg.message.encode()).hexdigest()
            if msg.msg_hash == localHash:
                m1 = Mess(nickname, "server-hash-return", localHash, "OK")
                m1Pickle = pickle.dumps(m1)
                client.send(m1Pickle)
            else:
                m1 = Mess(nickname, "server-hash-return", "", "NOK")
                m1Pickle = pickle.dumps(m1)
                client.send(m1Pickle)




def simple_send_to_server(msg):
    m1 = Mess(nickname, "server-hash-return", "", msg)
    m1Pickle = pickle.dumps(m1)
    client.send(m1Pickle)

def send(receiver, msg):
    message_not_send = True

    global server_response_flag
    server_response_flag = False

    hashtmp = hashlib.sha256(msg.encode()).hexdigest()
    m1 = Mess(nickname, receiver, hashtmp, msg)
    m1Pickle = pickle.dumps(m1)
    client.send(m1Pickle)

    wait_iterator = 0

    while not server_response_flag or wait_iterator > 10:
        time.sleep(0.5)
        wait_iterator += 1

    if wait_iterator > 10:
        print("server unreachable (send)")


    # client.send(m1Pickle)
    # rec = client.recv(4096)  # magic number
    # msg_back = pickle.loads(rec)
    # print("Message-received: {", msg_back.msg_sender, ",", msg_back.msg_receiver,
    #      ",", msg_back.msg_hash, ",", msg_back.message, "}")
    # if msg_back.message == "OK":
    #    message_not_send = False

    # message = msg.encode(FORMAT)
    # msg_length = len(message)
    # send_length = str(msg_length).encode(FORMAT)
    # send_length += b' ' * (HEADER_SIZE - len(send_length))
    # client.send(send_length)
    # client.send(message)


if __name__ == "__main__":
    print("[INFO:CLIENT] Starting client app...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[INFO:CLIENT] Connecting to server...")
    client.connect(ADDR)

    print("Enter your nickname")
    nickname = input()

    thread = threading.Thread(target=client_receiver, args=())
    thread.start()

    send_hello()

    connected = True
    while connected:
        print("Enter receiver:")
        user_input1 = input()
        print("Enter message:")
        user_input2 = input()
        if user_input1 == "quit" or user_input2 == "quit":
            connected = False
            send("", DISCONNECTED_MESSAGE)
        else:
            send(str(user_input1), str(user_input2))
