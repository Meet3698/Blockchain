import pymongo

class DB:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://Jack:Jack5972@blockchain.2n0ho.mongodb.net/p2p?retryWrites=true&w=majority")
        self.db = self.client['p2p']
        self.collection_nodes = self.db['nodes']
        self.collection_voter_details = self.db['voter_details']
