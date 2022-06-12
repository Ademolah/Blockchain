from solcx import compile_standard
import json
from web3 import Web3



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
chain_id = 5777
my_address = "0xa2A6b33F4937A8EC3B618591Aa693810Eb01d9B0"
my_privateKey = "0xed7f9aa35b2404a5739c9280aa42dfd23c0da5aa55ef0d6757786df89592bed6"

#create the contract in python

SimpleStorage = w3.eth.contract(abi = abi, bytecode=bytecode)

#get transactions count 
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)
