
from client import *
from server import *
from db import *
from constants import *
class p2p:
    peers = []

def main():
    db = DB()

    if db.collection_nodes.count() == 0:
        host = get_ip_address()
        p2p.peers.append(host)
        db.collection_nodes.insert_one({'node':host})
    else:
        nodes = db.collection_nodes.find()
        for node in nodes:
            if node == get_ip_address():
                p2p.peers.append(node['node'])
            else:
                db.collection_nodes.insert_one({'node':get_ip_address()})
                p2p.peers.append(get_ip_address())
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
                    sys.exit(0)
                except:
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

    