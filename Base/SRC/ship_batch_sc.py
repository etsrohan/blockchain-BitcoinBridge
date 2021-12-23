# IMPORT STATEMENTS
from web3 import Web3
import json

# ---------------------CONNECT TO SUPPLY CHAIN CONTRACT ON GANACHE---------------------
# web3.py instance - Connectiong to Ganache App
GANACHE_URL = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if w3.isConnected():
    print("\n[SUCCESS] Connected to the Ganache Blockchain Environment!")
    
# Getting smart conract information
with open('Contracts/SupplyChain.info', 'r') as file_object:
    contract_info = file_object.readlines()

supply_address = contract_info[0][:-1]
abi = json.loads(contract_info[1])

# Start deploying smart contract
print("\n[CONNECTING] Connecting to Supply Chain Contract...")

supplychain = w3.eth.contract(
    address = supply_address,
    abi = abi
)

w3.eth.default_account = w3.eth.accounts[0]
print("\n[SUCCESS] Connected to Supply Chain Smart Contract...")
# -----------------------------MAIN PROGRAM-----------------------------

# Get user input for delivery id
batch_id = int(input("Please enter the batch ID that finished processing: "))

# Send a transaction to confirm delivery
try:
    tx_hash = supplychain.functions.ship_batch(batch_id).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
except Exception as err:
    print("[ERROR] Something went wrong! Please check the batch ID to make sure it is valid!")
    print(err)