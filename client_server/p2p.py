# from client_server.client import *
# from client_server.constants import *
# from client_server.server import *

# import datetime
# import hashlib
# import json
# from flask import Flask, jsonify, request
# import requests
# from urllib.parse import urlparse
# from uuid import uuid4

class p2p:
    peers = ['127.0.0.1']

# while True:
#     try:
#         print("-" * 21 + "Trying to connect" + "-" * 21)

#         time.sleep(randint(RAND_TIME_START,RAND_TIME_END))

#         for peer in p2p.peers:
#             try:
#                 client = Client(peer)
#                 print(client)
#             except KeyboardInterrupt:
#                 sys.exit(0)
#             except:
#                 pass

#             if randint(1,5) ==1:
#                 try:
#                     server = Server()
#                 except KeyboardInterrupt:
#                     sys.exit(0)
#                 except:
#                     print("Couldn't start the server!")
#     except KeyboardInterrupt as e:
#         print(e)
#         sys.exit(0)
    