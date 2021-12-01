from constants import *
from db import *
from blockchain import *
from peer import *

class Server:

	def __init__(self,s_addr):
		try:
			self.connections = []
			self.peers = []

			self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)

			self.s.bind((host,port))
			self.s.listen(1)

			print("-" * 25 + " Server is running on " + host + "-" * 25)
			self.peers.append((s_addr[0],port))

			if get_ip_address() != p2p.peers[0]:
				p2p.peers = [] 
		
			db = DB()
			nodes = db.collection_nodes.find()

			url = 'http://' + str(host) + ':5000/get_chain'
			r = requests.get(url)
			
			for node in nodes:
				db.collection_nodes.update_one({'node' : node['node']},{ "$set": { 'node': host } })

			while True:
				connection, addr = self.s.accept()
				self.peers.append(addr)
				print('Peers are {}'.format(self.peers))

				c_thread = threading.Thread(target=self.handler, args=(connection,addr))
				c_thread.daemon = True
				c_thread.start()

				self.connections.append(connection)
				print('{} connected!!'.format(addr))
		except Exception as e:
			sys.exit()

	def handler(self,connection, addr):
		try:
			while True:
				data = connection.recv(byte_size)
				print("data recieved...",data)

				if data and data.decode('utf-8') == 'bye':
					self.disconnect_client(connection,addr)
					return
				elif data and data.decode('utf-8') == 'req':
					self.send_peers()
				else:
					sys.exit()
		except Exception as e:
			sys.exit()
	
	def disconnect_client(self,connection,addr):
		self.connections.remove(connection)
		self.peers.remove(addr)
		connection.close()
		self.send_peers()
		print('{} disconnected!!'.format(addr))

	def disconnect_server(self):
		self.s.close()

	def send_peers(self):
		peer_list = ""
		network = []
		for peer in self.peers:
			network.append(peer[0])
			peer_list = peer_list + str(peer[0]) + ","

		url = 'http://' + str(host) + ':5000/connect_node'
		r = requests.post(url, data = json.dumps({'peer' : network}))

		for connection in self.connections:
			data = peer_byte_difference + bytes(peer_list,'utf-8')
			connection.send(data)