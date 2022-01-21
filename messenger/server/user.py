class User:
    def __init__(self, connection_socket, ip_address):
        self.nickname = "?"  # UNIQ ACROSS whole server # probably nickname
        self.passwd_hash = "?"
        self.active = True

        self.conn_socket = connection_socket
        self.ip_address = ip_address
        self.thread = None


# to think about
class Admin(User):
    pass
