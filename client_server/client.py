from client_server.constants import *
from client_server.p2p import p2p


class Client:

    def __init__(self, addr):

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.connect((addr, PORT))

        thread_init = threading.Thread(target=self.send_message)
        thread_init.daemon = True
        thread_init.start()

        while True:
            data = self.s.recv(BYTE_SIZE)

            if not data:
                print("-" * 21 + " Server Failed " + "-" * 21)
                break
            if data[0:1] == b'\x11':
                print("Got Peers")
                self.update_peers(data[1:])
            else:
                print(str(data, 'utf-8'))

    def update_peers(self, peers):
        p2p.peers = str(peers, "utf-8").split(',')[:-1]

    def send_message(self):
        while True:
            self.s.send(bytes(input("Enter msg : "),'utf-8'))
