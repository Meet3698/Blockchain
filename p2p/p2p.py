
from client import *
from server import *
import pymongo

class p2p:
    peers = []
    client = pymongo.MongoClient("mongodb+srv://Jack:Jack5972@blockchain.2n0ho.mongodb.net/p2p?retryWrites=true&w=majority")
    db = client['p2p']
    collection = db['nodes']
    
    def get_ip_address():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    if collection.count() == 0:
        host = get_ip_address()
        print(host)
        peers.append(host)
        collection.insert_one({'node':host})
    else:
        nodes = collection.find()
        for node in nodes:
            peers.append(node['node'])
    print(peers)

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

    