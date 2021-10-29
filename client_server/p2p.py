from client_server.client import *
from client_server.constants import *
from client_server.server import *

class p2p:
    peers = ['127.0.0.1']


def main():

    while True:
        try:
            print("-" * 21 + "Trying to connect" + "-" * 21)

            time.sleep(randint(RAND_TIME_START,RAND_TIME_END))

            for peer in p2p.peers:
                try:
                    client = Client(peer)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass

                if randint(1,5) ==1:
                    try:
                        server = Server()
                    except KeyboardInterrupt:
                        sys.exit(0)
                    except:
                        print("Couldn't start the server!")
        except KeyboardInterrupt as e:
            print(e)
            sys.exit(0)

if __name__ == "__main__":
    main()