from client_server.constants import *

class Server:
     
    def __init__(self):
        try:
            self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

            self.connections = []
            self.peers = []

            self.s.bind((HOST,PORT))
            self.s.listen()

            print("-" * 21 + "Server running" + "-" * 21)

            self.run()
    
        except Exception as e:
            sys.exit()


    def handler(self, connection, a):

        try:
            while True:
                data = connection.recv(BYTE_SIZE)
                
                for connection in self.connections:
                    if data and data.decode('utf-8')[0].lower() == 'q':
                        self.disconnect(connection, a)
                        return 
        except Exception as e:
            sys.exit()        

    
    def disconnect(self, connection, a):
        self.connections.remove(connection)
        self.peers.remove(a)
        connection.close()
        self.send_peers()

        print("{}, disconnected".format(a))
        print("-" * 50)

    def run(self):
        while True:
            connection, a = self.s.accept()
            self.peers.append(a)

            print("Peers are {}".format(self.peers))

            self.send_peers()

            thread_connect = threading.Thread(target=self.handler, args=(connection, a))
            thread_connect.daemon = True
            thread_connect.start()

            self.connections.append(connection)

            print("{}, connected".format(a))
            print("-" * 50)

    def send_peers(self):
        peer_list = ""

        for peer in self.peers:
            peer_list = peer_list + str(peer[0]) + ","
        
        for connection in self.connections:
            data = PEER_BYTE_DIFFERENTIATOR + bytes(peer_list, 'utf-8')
            connection.send(data)

