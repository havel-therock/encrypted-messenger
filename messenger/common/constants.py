from enum import Enum, auto

HEADER_SIZE = 64
PORT = 6666
FORMAT = "utf-8"
SERVER = "127.0.1.1"


class RequestType(Enum):

    def _generate_next_value_(name, start, count, last_values):
        return name

    #  Clients requests for server
    LOG_IN = auto()
    REGISTER = auto()
    SEND_MSG = auto()
    DISCONNECT = auto()
    PONG = auto()  # answer to PING

    #  Server requests for client
    UPDATE_CONVERSATION = auto()
    USERNAME_TAKEN = auto()
    NEW_MESSAGE = auto()
    LOG_IN__OK = auto()
    SERVER_SHUTDOWN = auto()
    PING = auto()  # check if client alive
