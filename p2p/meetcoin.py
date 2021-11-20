from flask import Flask, jsonify, request, render_template
import flask
from blockchain import *
from peer import *
from server import *
from client import *
from db import *

from ecdsa import SigningKey, VerifyingKey

#Creating web-app 
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

#Creating an address for the node on port 5000
node_address = str(uuid4()).replace('-','')


blockchain = Blockchain()
db = DB()

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
    # nodes = [request.get_data().decode().split('=')[1]]
    req = json.loads(request.get_data())
    nodes = req['peer']
    blockchain.nodes = []

    print('In connect_node --- ',nodes)

    if nodes is None:
        return 'No Node', 400
    for node in nodes:
        print('Node --- ',node)
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

@app.route('/disconnect',methods = ['GET'])
def disconnect():
    print('Flag --- ',Blockchain.s_flag)
    return jsonify({'key' : Blockchain.s_flag}), 200
   
@app.route('/', methods = ['GET'])
def home():
    return render_template('index.html')

@app.route('/authenticate', methods = ['POST'])
def authenticate():
    req = json.loads(request.data.decode())
    voter_details = db.collection_voter_details.find_one({'voter_id' : req['voter_id']})
    if voter_details != None:
        if req['name'] == voter_details['name']:
            print(voter_details)
            if voter_details['pub_key'] == "":
                
                sk = SigningKey.generate()
                vk = sk.verifying_key
                vk2 = vk.to_string().hex()
            
                db.collection_voter_details.update_one({'voter_id' : voter_details['voter_id']},{ "$set": { 'pub_key': vk2 } })
                
                response = {
                'message' : 'You are successfully authenticated !!!',
                'priv_key' : 'Here is the private key --- ' + sk.to_string().hex()
            }
            else:
                response = {
                'message' : 'You are successfully authenticated !!!',
                'priv_key' : 'You already have a private key'
            }
            
            return jsonify(response), 200
        else:
            response = {
                'message' : 'Please enter name as per the voter ID',
                'flag' : 2
            }
            return jsonify(response), 200

    else:
        response = {
            'message' : 'Voter ID does not exist',
            'flag' : 1
        }
        return jsonify(response), 200        
                    

@app.route('/verify', methods = ['POST'])
def verify():
    req = json.loads(request.get_data())
    sk = SigningKey.from_string(bytes.fromhex(req['priv_key']))

    signature = sk.sign(b"Hello World!! This is a secret message.")
    vk = db.collection_voter_details.find_one({'voter_id' : 'abcd123'})['pub_key']
    vk2 = VerifyingKey.from_string(bytes.fromhex(vk))

    try:
        msg = vk2.verify(signature, b"Hello World!! This is a secet message.")
        return jsonify({})
    except:
        return jsonify({'message' : 'Jati re je'})


@app.route('/key_generation', methods = ['GET'])
def key_generation():
    print('In key generation')

    


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

app.run(host = get_ip_address(),port = 5000)