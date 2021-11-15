import socket
import threading
import sys
import time
from random import randint

byte_size = 1024
host = socket.gethostbyname(socket.gethostname())
port = 1234
peer_byte_difference = b'\x11'
rand_time_start = 1
rand_time_end = 2