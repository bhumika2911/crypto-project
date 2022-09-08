# Decentralized Housing Market System

This decentralized web-application is a basic implementation of a Housing Market System, based on a self-developed Blockchain backend. The Buyers can buy a listed Property by providing the seller's key, his own private key (generated within the program), and value paid upfront and his own address. In such a way, there is no need for middle-men in the process as the entire chain will be maintained by the foremost stakeholders themselves.

This blockchain has the following features:

- Zero Knowledge Proof Construction (Implemented from scratch)
- Proof of Work (PoW) algorithm
- Transactions with RSA cryptographic encryption

The Buyer's dashboard has the following features:

- Accounts generation using Public/Private key encryption (based on RSA algorithm)
- Generation of transactions with RSA encryption

# Dependencies

- [Anaconda's Python distribution](https://www.continuum.io/downloads) contains all the dependencies for the code to run.
- flask (```pip3 install flask```) - A lighweight python web framework
- flask_cors (```pip3 install flask_cors```) - Enable CORS for flask
- requests (```pip3 install requests```) - Parse http requests

# How to run the code

1. To start a blockchain node, go to ```blockchain``` folder and execute the command below:
   ```python blockchain.py -p 5000```
2. TO start the blockchain client, go to ```blockchain_client``` folder and execute the command below:
   ```python blockchain_client.py -p 8000```
3. You can access the blockchain frontend and blockchain client dashboards from your browser by going to localhost:5000 and localhost:8080 respectively

# Team Members:

Aman Mahajan (2018B3A70880H)
Bhumika Srivastava (2018B2AA0783H)