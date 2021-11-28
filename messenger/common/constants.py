import enum
from enum import Enum, auto

HEADER_SIZE = 64
PORT = 6666
FORMAT = "utf-8"
SERVER = "127.0.1.1"


class RequestType(Enum):

    #  Clients requests for server
    LOG_IN = auto
    REGISTER = auto
    SEND_MSG = auto
    DISCONNECT = auto

    #  Server requests for client
    UPDATE_CONVERSATION = auto

