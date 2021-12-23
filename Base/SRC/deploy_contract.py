# IMPORT STATEMENTS
from solcx import compile_source
from web3 import Web3
import json
import os

# ---------------------------------COMPILE SOLIDITY CODE---------------------------------
with open(os.path.join(os.getcwd(), "Contracts/SupplyChain.sol"), 'r') as file_obj:
    compiled_sol = compile_source(file_obj.read())

# checking the contents of the compiled contract
# print(compiled_sol.keys())

# Getting the contract interface
contract_id, contract_interface = compiled_sol.popitem()

# Getting the Contract bytecode/bin
bytecode = contract_interface['bin']
# getting the Contract abi
abi = contract_interface['abi']

# ---------------------------------DEPLOY SMART CONTRACT---------------------------------
# web3.py instance - Connectiong to Ganache App
GANACHE_URL = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if w3.isConnected():
    print("[SUCCESS] Connected to the Ganache Blockchain Environment!")

# Set first address as deployer for contract
w3.eth.default_account = w3.eth.accounts[0]

# Start deploying smart contract
print("[DEPLOYING] Deploying Supply Chain Contract...")

SupplyChainContract = w3.eth.contract(abi = abi, bytecode = bytecode)

# Submit transaction to deploy the contract then wait for receipt
tx_hash = SupplyChainContract.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("[SUCCESS] Contract Deployed!")
# ---------------------------------SAVE CONTRACT INFO---------------------------------
print("Saving Contract Info")

with open(os.path.join(os.getcwd(), 'Contracts/SupplyChain.info'), "w") as file_obj:
    file_obj.write(tx_receipt.contractAddress),
    file_obj.write("\n")
    file_obj.write(json.dumps(abi))
print('[SUCCESS] Supply Chain info saved!')

supplychain = w3.eth.contract(
    address = tx_receipt.contractAddress,
    abi = abi
)

print('[SUCCESS] Contract Deployed Successfully!!!')
