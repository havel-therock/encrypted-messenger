import socket
import threading
import hashlib
import pickle

class Mess:
  def __init__(self, msg_sender, msg_receiver, msg_hash, message):
    self.msg_sender = msg_sender
    self.msg_receiver = msg_receiver
    self.msg_hash = msg_hash
    self.message = message

#temporary databases

clients = []
nicknames = []

#header defines how much bytes will be in the next message, and have size of 64 bytes. So maximum size of next message will be 2^64 bytes
HEADER_SIZE = 64
FORMAT ="utf-8"
DISCONNECTED_MESSAGE = "###DISCONNECTED###"
PORT = 5050
SERVER_IP = socket.gethostbyname(socket.gethostname()) ### this sometimes return loopback ip addres instead of just private network ip 127... instead of 196
#to work this form internet, check for a public IP and put it here
ADDR = (SERVER_IP, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)




#figure out method for detecting disconnected clients which has not log out properly by sending DISCONNECT_MESSAGE
# probably ping  every 5 minutes all inactive user if they are online... If no response... remove them from active users list and kill their thread

def handle_client(conn, addr):
    print(f"[INFO] {addr} connected.")

    connected = True
    while connected:
        #msg_length = conn.recv(HEADER_SIZE).decode(FORMAT)
        msg_bits = conn.recv(4096)    #magic number
        if msg_bits:
            msg = pickle.loads(msg_bits)
            #msg_length = int(msg_length)
            #msg = conn.recv(msg_length).decode(FORMAT)
            if msg.message == DISCONNECTED_MESSAGE:
                connected = False
            # action need to be taken from here. For now just print messages and address which they come from
            print("[INFO] addr: ", addr, "Message received: {", msg.msg_sender, ",", msg.msg_receiver,
                  ",", msg.msg_hash, ",", msg.message, "}")

            #message-cases
            if msg.msg_receiver == "server-hello": #hello message
                clients.append(conn) #skleić client i nicknames w pary
                nicknames.append(msg.msg_sender)
                conn.send(pickle.dumps(Mess("server-hello-authentication", "", "", "OK")))
            elif msg.msg_receiver == "server-hash-return" and msg.message == "OK":
                #jest ok, doszla
                #zrzuca z kolejki niewysłane wiadomości o hashu który teraz powrócił
                print("message to ",msg.msg_sender, " was ok")
            elif msg.msg_receiver == "server-hash-return" and msg.message == "NOK":
                #nie jest ok, nie doszla
                print("message to ", msg.msg_sender, " was Nok")
            else:   #normal message
                localHash = hashlib.sha256(msg.message.encode()).hexdigest()
                if localHash == msg.msg_hash:
                    conn.send(pickle.dumps(Mess("server-authentication", "", "", "OK")))
                    for i in range(len(nicknames)):
                        if nicknames.__getitem__(i) == msg.msg_receiver:
                            send_message(msg, msg_bits, clients.__getitem__(i))
                else:
                    print("message is NOK")
                    conn.send(pickle.dumps(Mess("server-authentication", "", "", "NOK")))

    conn.close()


def send_message(msg,msg_bits,connection):
    print("Sending message {", msg.msg_sender, ",", msg.msg_receiver,
          ",", msg.msg_hash, ",", msg.message, "}")
    connection.send(msg_bits)


def start():
    server.listen()
    print(f"[INFO:SERVER] Server is listening on {SERVER_IP}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[INFO] ACTIVE CONNECTIONS: {threading.active_count() - 1}")

if __name__ == "__main__":
    print("[INFO:SERVER] Starting server...")
    print(socket.gethostname())
    start()

