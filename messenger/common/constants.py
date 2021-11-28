import enum
from enum import Enum, auto


class RequestType(Enum):

    #  Clients requests for server
    LOG_IN = auto
    REGISTER = auto
    SEND_MSG = auto
    DISCONNECT = auto

    #  Server requests for client
    UPDATE_CONVERSATION = auto
