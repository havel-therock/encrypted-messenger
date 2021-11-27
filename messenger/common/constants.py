from enum import Enum


class ClientRequestType(Enum):
    LOG_IN = 1
    REGISTER = 2
    SEND_MSG = 3
    DISCONNECT = 4


