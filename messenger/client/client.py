import socket

HEADER_SIZE = 64
PORT = 5050
FORMAT ="utf-8"
DISCONNECTED_MESSAGE = "###DISCONNECTED###"
SERVER="127.0.1.1"
ADDR = (SERVER, PORT)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER_SIZE - len(send_length))
    client.send(send_length)
    client.send(message)

if __name__ == "__main__":
    print("[INFO:CLIENT] Starting client app...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[INFO:CLIENT] Connecting to server...")
    client.connect(ADDR)

    connected = True
    while connected:
        user_input = input()
        if user_input == "quit":
            connected = False
            send(DISCONNECTED_MESSAGE)
        else:
            send(str(user_input))