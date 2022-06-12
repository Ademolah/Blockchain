from solcx import compile_standard
import json
from web3 import Web3
import os 


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"simpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    # solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

#get bytecodes
bytecode = compiled_sol["contracts"]["simpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#get abi 
abi = compiled_sol["contracts"]["simpleStorage.sol"]["SimpleStorage"]["abi"]

#connecting ganache 
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x010ae82e8EF6dd16EE41c85A71f2D8E80B6eF3BA"
#my_privateKey = "0xf83809eb85cacc3d9c09417a48286bb1a35045f18f3d93acbcb4ed36e4f87572"
my_privateKey = os.getenv("PRIVATE_KEY")
print(my_privateKey)

#create the contract in python

SimpleStorage = w3.eth.contract(abi = abi, bytecode=bytecode)

#get transactions count 
nonce = w3.eth.getTransactionCount(my_address)

#to create a transaction; a transaction occurs each time we change the state of our blockchain
#1. Build a transaction 
#2. Sign a transaction
#3. send a transaction 

transaction = SimpleStorage.constructor().buildTransaction(
    {"gasPrice": w3.eth.gas_price,"chainId": chain_id, "from": my_address, "nonce": nonce}
    )

signed_txn = w3.eth.account.signTransaction(transaction, private_key= my_privateKey)
