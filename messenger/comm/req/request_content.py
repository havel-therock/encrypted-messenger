class MessContent:
    def __init__(self, msg_sender, msg_receiver, msg_hash, message):
        self.msg_sender = msg_sender    # nickname
        self.msg_receiver = msg_receiver  # nickname # later change to chat_room_ID
        self.msg_hash = msg_hash        # message_hash
        self.message = message


class LogInContent:
    def __init__(self, nickname, passwd):
        self.nickname = nickname
        self.passwd = passwd
