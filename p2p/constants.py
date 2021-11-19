import socket
import threading
import sys
import time
from random import randint
import json
import requests

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

byte_size = 1024
host = get_ip_address()
port = 1234
peer_byte_difference = b'\x11'
rand_time_start = 1
rand_time_end = 2