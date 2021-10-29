from client_server.constants import *

class Server:

    def __init__(self):
        try:
            self.connections = []
            self.peers = []

            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.s.bind((HOST, PORT))
            self.s.listen(1)

            print("-" * 21 + "Server running" + "-" * 21)

            self.run()

        except Exception as e:
            print('Constructor',e)
            sys.exit(0)

    def handler(self, connection, a):

        try:
            while True:
                # connection.send()
                data = connection.recv(BYTE_SIZE)
                for connection in self.connections:
                    connection.send(data)
                if not data:
                    self.disconnect(connection, a)

        except Exception as e:
            print('handler',e)
            sys.exit(0)

    def disconnect(self, connection, a):
        self.connections.remove(connection)
        self.peers.remove(a[0])
        connection.close()
        print("{}, disconnected".format(a))
        print("-" * 50)
        self.send_peers()

    def run(self):
        while True:
            connection, a = self.s.accept()

            thread_connect = threading.Thread(target=self.handler, args=(connection, a))
            thread_connect.daemon = True
            thread_connect.start()

            self.connections.append(connection)
            self.peers.append(a[0])

            print(a," connected")
            print("-" * 50)

            self.send_peers()

    def send_peers(self):
        peer_list = ""

        for peer in self.peers:
            peer_list = peer_list + peer + ","

        for connection in self.connections:
            data = PEER_BYTE_DIFFERENTIATOR + bytes(peer_list, 'utf-8')
            connection.send(data)
