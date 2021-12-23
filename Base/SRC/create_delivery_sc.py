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
print("\n[SUCCESS] Connected to Supply Chain Smart Contract...")
# -----------------------------MAIN PROGRAM-----------------------------

def create_order(material: int, supplier: str, weight: int, cost: int) -> None:
    """This function sends a transaction to create a delivery order for materials
    in the supply chain smart contract

    Args:
        material (int): 0 -> Cotton, 1 -> Ethylene, anything else is invaid
        supplier (str): Name of the supplier for the materials
        weight (int): weight of the materials ordered in grams
        cost (int): cost of the materials ordered in grams
    """
    
    if material not in [0, 1]:
        print('[ERROR] Material must be either Cotton or Ethylene i.e. 0 or 1')
        exit()
    
    if weight <= 0:
        print('[ERROR] Weight of materials delivered must be positive.')
        exit()
        
    if cost <= 0:
        print('[ERROR] Cost of materials delivered must be positive.')
        exit()
        
    tx_hash = supplychain.functions.create_delivery_order(
        material,
        supplier,
        weight,
        cost).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print('[SUCCESS] Sent a delivery order. Please wait for confirmation on event listener.')
    
# Getting employee id
employee_num = int(input("Please enter your employee id [1-9]: "))
# Set default address
w3.eth.default_account = w3.eth.accounts[employee_num]
    
# Getting the user input for delivery details
material = int(input("Please enter the material for delivery [0: Cotton, 1: Ethylene]: "))
supplier = input("Please enter the Name of the supplier: ")
weight = int(input("Please enter the Weight of materials ordered in grams (g): "))
cost = int(input("Please enter the Cost of delivery in cents ($1  = 100 cents): "))

# Send the request for delivery
create_order(material, supplier, weight, cost)