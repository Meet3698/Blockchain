import socket, threading, sys, time
from random import randint

BYTE_SIZE = 1024
HOST = '0.0.0.0'
PORT = 5000
PEER_BYTE_DIFFERENTIATOR = b'\x11'
RAND_TIME_START = 1
RAND_TIME_END = 2
REQUEST_STRING = "req"