class User:
    def __init__(self, user_id, connection_socket, ip_addr, **kwargs):
        # self.user_active = True
        self.user_id = user_id
        self.user_passwd = ""
        self.conn_socket = connection_socket
        self.ip_addr = ip_addr
        self.conn_status = "active"  # active|disconnected
        self.thread = None
        if "conn_status" in kwargs:
            self.conn_status = kwargs["conn_status"]
