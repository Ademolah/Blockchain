from solcx import compile_standard
import json
from web3 import Web3
import os 
from dotenv import load_dotenv

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

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
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/91030e0778df4696aa19e04d08b2d465"))
chain_id = 4
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
#my_privateKey = "0xbb733f612a0bc6341f72a5dce9a7ee1906098746578eb0b2b30257d91aac8e9e"
my_privateKey = os.getenv("PRIVATE_KEY1")

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

#signing our transaction
signed_txn = w3.eth.account.signTransaction(transaction, private_key = my_privateKey)


#send transaction to ganache
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

#working with the contract
simple_storage = w3.eth.contract(address = txn_receipt.contractAddress, abi = abi)
print(simple_storage.functions.retrieve().call())

store_txn = simple_storage.functions.store(12).buildTransaction(
    {"gasPrice": w3.eth.gas_price,"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
    )

signed_store_txn = w3.eth.account.signTransaction(store_txn, private_key = my_privateKey)

print("Deploying contract...")
send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_txn_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)
print("Deployed !")

print(simple_storage.functions.retrieve().call())






