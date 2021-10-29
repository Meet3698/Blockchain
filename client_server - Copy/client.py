from client_server.constants import *
from client_server.p2p import *

class Client:

    def __init__(self, addr):

        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.connect((addr,PORT))

        self.previous_data = None

        thread_init = threading.Thread(target=self.send_message)
        thread_init.daemon = True
        thread_init.start()

        while True:
            thread_recv = threading.Thread(target=self.recieve_message)
            thread_recv.start()
            thread_recv.join()

            data = self.recieve_message()

            if not data:
                print("-" * 21 + " Server Failed " + "-" * 21)
                break
            elif data[0:1] == b'\x11':
                print("Got Peers")
                self.update_peers(data[1:])


    def recieve_message(self):
        try:
            print("Recieving --------")
            data = self.s.recv(BYTE_SIZE)
            print(data.decode("utf-8"))

            print("\nRecieved messge on the client side is:")

            if self.previous_data != data:
                self.previous_data = data

            return data
        
        except KeyboardInterrupt:
            self.send_disconnect_signal()
    

    def update_peers(self, peers):
        p2p.peers = str(peers, "utf-8").split(',')[:-1]

    
    def send_message(self):
        try:
            self.s.send(REQUEST_STRING.encode('utf-8'))
        
        except KeyboardInterrupt as e:
            self.send_disconnect_signal()
            return
    

    def send_disconnect_signal(self):
        print("Disconnected from server")
        self.s.send("q".encode('utf-8'))
        sys.exit()

