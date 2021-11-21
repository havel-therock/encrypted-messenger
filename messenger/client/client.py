import socket
import hashlib
import pickle

class Mess:
  def __init__(self, msg_sender, msg_reciver, msg_hash, message):
    self.msg_sender = msg_sender
    self.msg_reciver = msg_reciver
    self.msg_hash = msg_hash
    self.message = message

HEADER_SIZE = 64
PORT = 5051
FORMAT ="utf-8"
DISCONNECTED_MESSAGE = "###DISCONNECTED###"
SERVER="127.0.1.1"
ADDR = (SERVER, PORT)


def send_hello():
    reciver = "server-hello"

    m1 = Mess(nickname, reciver, "", "hello server my name is "+nickname)
    m1Pickle = pickle.dumps(m1)
    client.send(m1Pickle)
    rec = client.recv(4096)  # magic number
    msg_back = pickle.loads(rec)
    print("Message-recived: {", msg_back.msg_sender, ",", msg_back.msg_reciver,
          ",", msg_back.msg_hash, ",", msg_back.message, "}")

def send(msg):
    message_not_send = True
    
    while message_not_send:
        reciver = "reciver112"
        hashtmp = hashlib.sha256(msg.encode()).hexdigest()
        m1 = Mess(nickname, reciver, hashtmp, msg)
        m1Pickle = pickle.dumps(m1)
        client.send(m1Pickle)
        rec = client.recv(4096)     #magic number
        msg_back = pickle.loads(rec)
        print("Message-recived: {", msg_back.msg_sender, ",", msg_back.msg_reciver,
          ",", msg_back.msg_hash, ",", msg_back.message, "}")
        if msg_back.message == "OK":
            message_not_send = False
            
    #message = msg.encode(FORMAT)
    #msg_length = len(message)
    #send_length = str(msg_length).encode(FORMAT)
    #send_length += b' ' * (HEADER_SIZE - len(send_length))
    #client.send(send_length)
    #client.send(message)

if __name__ == "__main__":
    print("[INFO:CLIENT] Starting client app...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[INFO:CLIENT] Connecting to server...")
    client.connect(ADDR)

    print("Enter your nickname")
    nickname = input()
    
    send_hello()
    
    connected = True
    while connected:
        user_input = input()
        if user_input == "quit":
            connected = False
            send(DISCONNECTED_MESSAGE)
        else:
            send(str(user_input))
            