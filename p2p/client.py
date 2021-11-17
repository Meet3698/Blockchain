from time import sleep
from constants import *
import requests

from p2p import p2p

class Client:

	def __init__(self,addr):

		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
		self.s.connect((addr,port))

		i_thread = threading.Thread(target=self.send_message)
		i_thread.daemon = True
		i_thread.start()

		while True:

			# r_thread = threading.Thread(target=self.send_message)
			# r_thread.start()
			# r_thread.join()

			data = self.recieve_message()

			if not data:
				print('Server Failed!!')
				raise SystemExit  
			elif data[0:1] == b'\x11':
				print('Got peers\n')
				self.update_peers(data[1:])

	def send_message(self):
		try:
			# data = str(input('Enter "req" to request data\n\n Enter "bye" to disconnect\n\n'))
			# self.s.send(data.encode('utf-8'))
			self.s.send('req'.encode('utf-8'))
		except KeyboardInterrupt as e:
			print('Disconnected From the server')
			self.s.send('bye'.encode('utf-8'))
			sys.exit()
	
	def recieve_message(self):
		try:
			data = self.s.recv(byte_size)
			print('Recieved data : {}'.format(data))
			return data
		except KeyboardInterrupt:
			print('Disconnected From the server')
			self.s.send('bye'.encode('utf-8'))
			sys.exit()

	def update_peers(self,peers):
		p2p.peers = str(peers,'utf-8').split(',')[:-1]
		query = 'http://' + str(host) + ':5000/connect_node'
		r = requests.get(query)

		print(r)