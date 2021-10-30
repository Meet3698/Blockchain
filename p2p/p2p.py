from constants import *
from client import *
from server import *

class p2p:
    peers = ['192.168.11.53']

def main():
    while True:
        try:
            print("-"*25 + " Trying to connect " + "-"*25)
            time.sleep(randint(rand_time_start,rand_time_end))

            for peer in p2p.peers: 
                try:
                    Client(peer)
                except KeyboardInterrupt:
                    sys.exit(0)
                except SystemExit:
                    sys.exit(0)
                except:
                    pass

                try:
                    Server()
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass

        except KeyboardInterrupt as e:
            sys.exit(0)
if __name__ == "__main__":
    main()