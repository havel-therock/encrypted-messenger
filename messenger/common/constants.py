from enum import Enum

HEADER_SIZE = 64
PORT = 6665
FORMAT = "utf-8"
SERVER = "127.0.1.1"


class RequestType(Enum):

    #  Clients requests for server
    LOG_IN = 1
    REGISTER = 2
    SEND_MSG = 3
    DISCONNECT = 4

    #  Server requests for client
    UPDATE_CONVERSATION = 5
    USERNAME_TAKEN = 6
    NEW_MESSAGE = 7
    LOG_IN__OK = 8
    SERVER_SHUTDOWN = 9
