"""
Created on Thu Oct 21 17:07:26 2021

@author: Meet Patel
"""

#importing Libraries

import datetime
import hashlib
import json
import requests
from urllib.parse import urlparse
from uuid import uuid4
import socket
# from peer import *

#Creating Blockchain
class Blockchain:
    s_flag = None
    #Intializing Genesis Block and Empty Chain
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = []
        

    #creating block and add to the chain
    def create_block(self, proof, previous_hash):
        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : str(datetime.datetime.now()),
            'proof' : proof,
            'previous_hash' : previous_hash,
            'transactions' : self.transactions
            }
        self.transactions = []
        self.chain.append(block)
        return block
    
    #return previous block 
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self,block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        
        while block_index < len(chain):
            block = chain[block_index]
            
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']
            
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, pub_key, house, name):
        self.transactions.append({
            'pub_key' : pub_key,
            'house' : house,
            'name' : name,
        })
        previous_block =  self.get_previous_block() 
        return previous_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        url = parsed_url.path + ':5000'
        print('URL in add_node --- ',url)
        self.nodes.append(url)
        print('In add_node ---',self.nodes)

    def replace_chain(self):
        network = self.nodes
        print('In replace chain --- network --- ', network)        
        longest_chain = None
        max_length = len(self.chain)

        for nodes in network:
            response = requests.get(f'http://{nodes}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
                else:
                    pass
        if longest_chain:
            self.chain = longest_chain
            return True
        else:
            return False