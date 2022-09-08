
''' DECENTALIZED HOUSING MARKET
    Members: Aman Mahajan (2018B3A70880H)
             Bhumika Srivastava (2018B2AA0783H)'''

from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

import random

MINING_AADHAR = "999999999999"
MINING_SENDER = "THE BLOCKCHAIN"
MINING_REWARD = 1
MINING_DIFFICULTY = 2

class Seller:

    def __init__(self):

        #This is the confidential data that will be protected and verified through Zero Knowledge Proof (ZKP)
        self.aadhar_seller = random.randint(100000000000, 999999999999)

        self.propprice = 10

    def zkpVerifyChallengeSeller(c, y, p, cipher1):

        cipher2 =  (c*y)%p
        if cipher2 == cipher1:
            # Alice is atleast partially convinced that Bob knows x
            return True
        else:
            return False

    def verify_transactions_zkp_seller(self):

        g = 961
        p = 997
        # convert string to a number
        x = self.aadhar_seller
        y = pow(g, x, p)
        '''BOB (this function) possesses secret information x'''

        # We are running the ZKP algorithm for 6 rounds
        for i in range(0,5):
            r = random.randrange(2, 100)
            c = pow(g, r, p) # (g^r) mod p
            cipher1 = pow(g, ((x+r)%(p-1)), p)
            if not self.zkpVerifyChallengeBuyer(c, y, p, cipher1):
                print("FATAL ERROR: ZERO KNOWLEDGE PROOF VERIFICATION FAILED")
                return False
        return True

class Buyer:

    def __init__(self):

        #This is the confidential data that will be protected and verified through Zero Knowledge Proof (ZKP)
        self.uniqueID = random.randint(100000000000, 999999999999)
        self.aadhar_buyer = random.randint(100000000000, 999999999999)

        self.bankbal = 10000

    def zkpVerifyChallengeBuyer(c, y, p, cipher1):

        cipher2 =  (c*y)%p
        if cipher2 == cipher1:
            # Alice is atleast partially convinced that Bob knows x
            return True
        else:
            return False

    def verify_transactions_zkp_buyer(self):

        g = 961
        p = 997
        # convert string to a number
        x = self.aadhar_buyer
        y = pow(g, x, p)
        '''BOB (this function) possesses secret information x'''

        # We are running the ZKP algorithm for 6 rounds
        for i in range(0,5):
            r = random.randrange(2, 100)
            c = pow(g, r, p) # (g^r) mod p
            cipher1 = pow(g, ((x+r)%(p-1)), p)
            if not self.zkpVerifyChallengeBuyer(c, y, p, cipher1):
                print("FATAL ERROR: ZERO KNOWLEDGE PROOF VERIFICATION FAILED")
                return False
        return True



class Blockchain:

    def __init__(self):

        self.transactions = []
        self.chain = []
        #Generate random number to be used as node_id
        self.node_id = str(uuid4()).replace('-', '')
        #Create genesis block
        self.create_block(0, '00')


    def verify_transaction_signature(self, sender_address, signature, transaction):
        """
        Check that the provided signature corresponds to transaction
        signed by the public key (sender_address)
        """
        #sender_address=Seller.aadhar
        public_key = RSA.importKey(binascii.unhexlify(sender_address))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA.new(str(transaction).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(signature))


    def submit_transaction(self, sender_address, recipient_address, value, signature):
        """
        Add a transaction to transactions array if the signature verified
        """
        #sender_address=Seller.aadhar
        transaction = OrderedDict({'sender_address': sender_address,
                                   'recipient_address': recipient_address,
                                   'value': value})

        #Reward for mining a block
        #if sender_address == Seller.aadhar:
        if sender_address == MINING_AADHAR:
            self.transactions.append(transaction)
            return len(self.chain) + 1
        #Manages transactions from wallet to another wallet
        else:
            print("CASE")
            transaction_verification = self.verify_transaction_signature(sender_address, signature, transaction)
            if transaction_verification:
                self.transactions.append(transaction)
                return len(self.chain) + 1
            else:
                return False


    def create_block(self, nonce, previous_hash):
        """
        Add a block of transactions to the blockchain
        """
        block = {'block_number': len(self.chain) + 1,
                 'timestamp': time(),
                 'transactions': self.transactions,
                 'nonce': nonce,
                 'previous_hash': previous_hash}

        # Reset the current list of transactions
        self.transactions = []

        self.chain.append(block)
        return block


    def hash(self, block):
        """
        Create a SHA-256 hash of a block
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()


    def proof_of_work(self):
        """
        Proof of work algorithm
        """
        last_block = self.chain[-1]
        last_hash = self.hash(last_block)

        nonce = 0
        while self.valid_proof(self.transactions, last_hash, nonce) is False:
            nonce += 1

        return nonce


    def valid_proof(self, transactions, last_hash, nonce, difficulty=MINING_DIFFICULTY):
        """
        Check if a hash value satisfies the mining conditions. This function is used within the proof_of_work function.
        """
        guess = (str(transactions)+str(last_hash)+str(nonce)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:difficulty] == '0'*difficulty

# Instantiate the Node
app = Flask(__name__)
CORS(app)

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/configure')
def configure():
    return render_template('./configure.html')



@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    #sender_address=Seller.aadhar
    values = request.form
    # Check that the required fields are in the POST'ed data
    required = ['sender_address', 'recipient_address', 'amount', 'signature']
    if not all(k in values for k in required):
        return 'Missing values', 400
    # Create a new Transaction
    transaction_result = blockchain.submit_transaction(values['sender_address'], values['recipient_address'], values['amount'], values['signature'])

    if transaction_result == False:
        response = {'message': 'Invalid Transaction!'}
        return jsonify(response), 406
    else:
        response = {'message': 'Transaction will be added to Block '+ str(transaction_result)}
        return jsonify(response), 201


@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    #Get transactions from transactions pool
    transactions = blockchain.transactions

    response = {'transactions': transactions}
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.chain[-1]
    nonce = blockchain.proof_of_work()

    # We must receive a reward for finding the proof.
    global MINING_AADHAR
    MINING_AADHAR =  str(random.randint(100000000000, 999999999999))
    # print("Aadhar value: ", MINING_AADHAR)
    blockchain.submit_transaction(sender_address=MINING_AADHAR, recipient_address=blockchain.node_id, value=MINING_REWARD, signature="")

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(nonce, previous_hash)

    response = {

        'message': "New Block Forged",
        'block_number': block['block_number'],
        'transactions': block['transactions'],
        'nonce': block['nonce'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/nodes/get', methods=['GET'])
def get_nodes():
    nodes = list(blockchain.nodes)
    response = {'nodes': nodes}
    return jsonify(response), 200



if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)