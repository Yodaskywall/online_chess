import socket
import pickle
HEADERSIZE = 10

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.108"
        self.port = 25565
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2096).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.pickle_receive()
        except socket.error as e:
            print(e)

    def pickle_send(self, object):
        msg = pickle.dumps(object)
        msg = bytes(f"{len(msg):<{HEADERSIZE}}", "utf-8") + msg
        self.client.send(msg)

    def pickle_receive(self):
        full_msg = b''
        new_msg = True
        while True:
            msg = self.client.recv(16)

            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False

            full_msg += msg

            if len(full_msg) - HEADERSIZE == msglen:
                object = pickle.loads(full_msg[HEADERSIZE:])
                return object
