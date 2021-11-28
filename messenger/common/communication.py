class Mess:
  def __init__(self, msg_sender, msg_reciver, msg_hash, message):
    self.msg_sender = msg_sender
    self.msg_reciver = msg_reciver
    self.msg_hash = msg_hash
    self.message = message


class LogIn:
    def __init__(self, email, passwd):
        self.email = email
        self.passwd = passwd

class Request:
    def __init__(self, request_type, content):
        self.request_type = request_type  # class RequestType
        self.content = content  # Any class

