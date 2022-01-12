# IMPORT STATEMENTS
from solcx import compile_source
from web3 import Web3
import json
import os

# ---------------------------------COMPILE SOLIDITY CODE---------------------------------
with open(os.path.join(os.getcwd(), "Contracts/SupplyChain.sol"), 'r') as file_obj:
    compiled_supply = compile_source(file_obj.read())
    
with open(os.path.join(os.getcwd(), "Contracts/TransactionBridge.sol"), 'r') as file_obj:
    compiled_bridge = compile_source(file_obj.read())

# checking the contents of the compiled contract
# print(compiled_sol.keys())

# SUPPLY CHAIN CONTRACT
# Getting the contract interface
contract_id, contract_interface = compiled_supply.popitem()

# Getting the Contract bytecode/bin
bytecode_supply = contract_interface['bin']
# getting the Contract abi
abi_supply = contract_interface['abi']

# TRANSACTION BRIDGE CONTRACT
# Getting the contract interface
contract_id, contract_interface = compiled_bridge.popitem()

# Getting the Contract bytecode/bin
bytecode_bridge = contract_interface['bin']
# getting the Contract abi
abi_bridge = contract_interface['abi']

# ---------------------------------DEPLOY SMART CONTRACT---------------------------------
# web3.py instance - Connectiong to Ganache App
GANACHE_URL = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

GANACHE_URL2 = "HTTP://127.0.0.1:7546"
w32 = Web3(Web3.HTTPProvider(GANACHE_URL2))

if w3.isConnected():
    print("[SUCCESS] Connected to the Supply Chain Ganache Blockchain Environment!")
    
if w32.isConnected():
    print("[SUCCESS] Connected to the Transaction Bridge Ganache Blockchain Environment!")

# Set first address as deployer for contract
w3.eth.default_account = w3.eth.accounts[0]
w32.eth.default_account = w32.eth.accounts[0]

# Start deploying smart contract
# Supply Chain
print("[DEPLOYING] Deploying Supply Chain Contract...")

SupplyChainContract = w3.eth.contract(abi = abi_supply, bytecode = bytecode_supply)

# Submit transaction to deploy the contract then wait for receipt
tx_hash = SupplyChainContract.constructor().transact()
tx_receipt_supply = w3.eth.wait_for_transaction_receipt(tx_hash)

print("[SUCCESS] Supply Chain Contract Deployed!")

# Transaction Bridge
print("[DEPLOYING] Deploying Transaction Bridge Contract...")

TransactionBridgeContract = w32.eth.contract(abi = abi_bridge, bytecode = bytecode_bridge)

# Submit transaction to deploy the contract then wait for receipt
tx_hash = TransactionBridgeContract.constructor().transact()
tx_receipt_bridge = w32.eth.wait_for_transaction_receipt(tx_hash)

print("[SUCCESS] Transaction Bridge Contract Deployed!")
# ---------------------------------SAVE CONTRACT INFO---------------------------------
# Supply Chain
print("Saving Supply Chain Contract Info")

with open(os.path.join(os.getcwd(), 'Contracts/SupplyChain.info'), "w") as file_obj:
    file_obj.write(tx_receipt_supply.contractAddress),
    file_obj.write("\n")
    file_obj.write(json.dumps(abi_supply))
print('[SUCCESS] Supply Chain info saved!')

supplychain = w3.eth.contract(
    address = tx_receipt_supply.contractAddress,
    abi = abi_supply
)

print('[SUCCESS] Supply Chain Contract Deployed Successfully!!!')

# Transaction Bridge
print("Saving Transaction Bridge Contract Info")

with open(os.path.join(os.getcwd(), 'Contracts/TransactionBridge.info'), "w") as file_obj:
    file_obj.write(tx_receipt_bridge.contractAddress),
    file_obj.write("\n")
    file_obj.write(json.dumps(abi_bridge))
print('[SUCCESS] Supply Chain info saved!')

transaction_bridge = w32.eth.contract(
    address = tx_receipt_bridge.contractAddress,
    abi = abi_supply
)

print('[SUCCESS] Transaction Bridge Contract Deployed Successfully!!!')
