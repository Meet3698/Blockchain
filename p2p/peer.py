
from client import *
from server import *
from db import *

class p2p:
    peers = []

def main():
    db = DB()
    
    def get_ip_address():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    if db.collection.count() == 0:
        host = get_ip_address()
        p2p.peers.append(host)
        db.collection.insert_one({'node':host})
    else:
        nodes = db.collection.find()
        for node in nodes:
            p2p.peers.append(node['node'])
    print('p2p peers -- ',p2p.peers)

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
                    if randint(1,10) == 7:
                        pass
                except:
                    if randint(1,10) == 7:
                        pass

                try:
                    Server(p2p.peers)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass

        except KeyboardInterrupt as e:
            sys.exit(0)

if __name__ == "__main__":
    main()

    