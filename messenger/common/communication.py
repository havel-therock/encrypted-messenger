class Mess:
  def __init__(self, msg_sender, msg_reciver, msg_hash, message):
    self.msg_sender = msg_sender
    self.msg_reciver = msg_reciver
    self.msg_hash = msg_hash
    self.message = message


class Content:
    def __init__(self):
        pass


class ClientRequest:
    def __init__(self, request_type, content, receiver):  # request_type mandatory
        self.request_type = request_type  # class ClientRequestType
        self.content = content  # Any class


class ServerRequest:
    pass
