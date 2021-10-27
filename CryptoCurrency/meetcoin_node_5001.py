"""
Created on Thu Oct 21 17:07:26 2021

@author: Meet Patel
"""

#importing Libraries

import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from urllib.parse import urlparse
from uuid import uuid4

#Creating Blockchain
class Blockchain:
    
    #Intializing Genesis Block and Empty Chain
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
    
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

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender' : sender,
            'receiver' : receiver,
            'amount' : amount
        })
        previous_block =  self.get_previous_block() 
        return previous_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
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
        if longest_chain:
            self.chain = longest_chain
            return True





#Creating web-app
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

#Creating an address for the node on port 5000
node_address = str(uuid4()).replace('-','')


blockchain = Blockchain()

@app.route('/mine_block',methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address, receiver='Meet', amount=1)
    block = blockchain.create_block(proof, previous_hash)
    
    response = {
            'message' : 'Congratulations!!! You have just mined a block',
            'index' : block['index'],
            'timestamp' : block['timestamp'],
            'proof' : block['proof'],
            'previous_hash' : block['previous_hash'],
            'transactions' : block['transactions']
        }
    
    return jsonify(response), 200

@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {
            'chain' : blockchain.chain,
            'length' : len(blockchain.chain)
        }
    
    return jsonify(response), 200

@app.route('/is_chain_valid', methods = ['GET'])
def is_chain_valid():
    is_chain_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_chain_valid:
        response = {'message' : 'All good! Blockchain is Valid'}
    else:
        response = {'message' : 'We have a problem. Blockchain is not valid'}
    
    return jsonify(response), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    keys = json.loads(request.get_data())
    transaction_keys = ['sender','receiver','amount']
    if not all ( key in keys for key in transaction_keys):
        return 'Some elements of the transaction are missing!!', 400
    index = blockchain.add_transaction(keys['sender'],keys['receiver'],keys['amount'])
    response = {
        'message' : f'This transaction will be added to block {index}'
    }

    return jsonify(response), 201


#Decentralization

@app.route('/connect_node', methods = ['POST'])
def connect_node():
    nodes = json.loads(request.get_data())['nodes']
    
    if nodes is None:
        return 'No Node', 400
    for node in nodes:
        blockchain.add_node(node)
    
    response = {
        'message' : 'All the nodes are now connected, The Meetcoin blockchain contains the following nodes : }',
        'total_nodes' : list(blockchain.nodes)
    }

    return jsonify(response), 201

@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {
            'message' : 'The nodes has different nodes so chain was replaced by longer chain',
            'new_chain' : blockchain.chain
        }
    else:
        response = {
            'message' : 'All good!! The chain is the largest chain',
            'actual_chain' : blockchain.chain    
        }
    
    return jsonify(response), 200

app.run(host = '127.0.0.1',port = 5001)