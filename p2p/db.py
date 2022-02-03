import pymongo

class DB:
    def __init__(self):
        self.client = pymongo.MongoClient("<API>")
        self.db = self.client['p2p']
        self.collection_nodes = self.db['nodes']
        self.collection_voter_details = self.db['voter_details']
