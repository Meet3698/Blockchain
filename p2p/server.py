from constants import *

class Server:

	def __init__(self):
		try:
			self.connections = []
			self.peers = []

			self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)

			self.s.bind((host,port))
			self.s.listen(1)

			print("-" * 25 + " Server is running on " + host + "-" * 25)

			while True:
				connection, addr = self.s.accept()
				
				self.peers.append(addr)
				print('Peers are {}'.format(self.peers))

				c_thread = threading.Thread(target=self.handler, args=(connection,addr))
				c_thread.daemon = True
				c_thread.start()

				self.connections.append(connection)
				self.peers.append(addr)
				print('{} connected!!'.format(addr))
		except Exception as e:
			sys.exit()

	def handler(self,connection, addr):
		try:
			while True:
				data = connection.recv(byte_size)
				print("data recieved...",data)

				if data and data.decode('utf-8') == 'bye':
					self.disconnect(connection,addr)
					return
				elif data and data.decode('utf-8') == 'req':
					self.send_peers()
				else:
					sys.exit()
		except Exception as e:
			sys.exit()
	
	def disconnect(self,connection,addr):
		self.connections.remove(connection)
		self.peers.remove(addr)
		connection.close()
		self.send_peers()
		print('{} disconnected!!'.format(addr))

	def send_peers(self):
		peer_list = ""
		for peer in self.peers:
			peer_list = peer_list + str(peer[0]) + ","

		for connection in self.connections:
			data = peer_byte_difference + bytes(peer_list,'utf-8')
			connection.send(data)