class Mess:
  def __init__(self, msg_sender, msg_reciver, msg_hash, message):
    self.msg_sender = msg_sender    # nickname
    self.msg_reciver = msg_reciver  # nickname
    self.msg_hash = msg_hash        # message_hash
    self.message = message


class LogIn:
    def __init__(self, nickname, passwd):
        self.nickname = nickname
        self.passwd = passwd

class Request:
    def __init__(self, request_type, content):
        self.request_type = request_type  # class RequestType
        self.content = content  # Any class

