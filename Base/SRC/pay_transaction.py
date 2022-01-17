# IMPORT STATEMENTS
from web3 import Web3
import json

# ---------------------CONNECT TO SUPPLY CHAIN CONTRACT ON GANACHE---------------------
# web3.py instance - Connectiong to Ganache App
GANACHE_URL = "HTTP://127.0.0.1:7546"
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if w3.isConnected():
    print("\n[SUCCESS] Connected to the Ganache Blockchain Environment!")
    
# Getting smart conract information
with open('Contracts/TransactionBridge.info', 'r') as file_object:
    contract_info = file_object.readlines()

bridge_address = contract_info[0][:-1]
abi = json.loads(contract_info[1])

# Start deploying smart contract
print("\n[CONNECTING] Connecting to Supply Chain Contract...")

transactionbridge = w3.eth.contract(
    address = bridge_address,
    abi = abi
)

w3.eth.default_account = w3.eth.accounts[0]
print("\n[SUCCESS] Connected to Supply Chain Smart Contract...")
# -----------------------------MAIN PROGRAM-----------------------------
# Send a blockchain transaction to pay for items
receipt_number = int(input(
    """\rPlease enter the Receipt Number if item is part of another transaction
       \ror '-1' if you want to start a new transaction..."""))
try:
    tx_hash = transactionbridge.functions.pay_transaction(receipt_number).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
except Exception as err:
    print("[ERROR] Something went wrong! Please check the fabric and apparel!")
    print(err)
print(transactionbridge.functions.get_state(111).call())