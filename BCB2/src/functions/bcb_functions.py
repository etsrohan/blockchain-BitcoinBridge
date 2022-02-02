"""
This file is used to store different functions that will be useful to the functionality
of the Bitcoin Bridge system.
"""
import os
import json
from solcx import compile_source
from web3 import Web3
from bit import PrivateKeyTestnet
from typing import List, Tuple

class BitcoinBridgeGanache:
    """This class contains several methods and variables that help in the following functionality
    for the Bitcoin Bridge Blockchain Project.
    1) Deploy Smart Contracts: deploy_contracts method deploys both the SupplyChain and BitcoinBridge
    contracts onto ganache"""
    
    def __init__(self):
        # Instance Variables
        # SUPPLY CHAIN
        self.supply_chain_address = None
        self.supply_chain_abi = None
        self.supply_chain_bytecode = None
        self.supply_chain_url = "HTTP://127.0.0.1:7545"
        self.supply_chain_w3 = None
        self.supply_chain_contract = None
        # BRIDGE
        self.bridge_address = None
        self.bridge_abi = None
        self.bridge_bytecode = None
        self.bridge_url = "HTTP://127.0.0.1:7546"
        self.bridge_w3 = None
        self.bridge_contract = None
        # BITCOIN
        
    def deploy_contracts(self) -> None:
        """Compiles, deploys and saves the supply chain and bitcoin bridge contracts onto
        two separate ethereum blockchains.
        contract .sol files located in contract folder.
        """
        with open("contracts/SupplyChain.sol", "r") as file_object:
            compiled_supply = compile_source(file_object.read())
        
        with open("contracts/TransactionBridge.sol", "r") as file_object:
            compiled_bridge = compile_source(file_object.read())
            
        # checking the contents of the compiled contract
        # print(compiled_sol.keys())

        # SUPPLY CHAIN CONTRACT
        # Getting the contract interface
        _, contract_interface = compiled_supply.popitem()

        # Getting the Contract bytecode/bin
        self.supply_chain_bytecode = contract_interface['bin']
        # getting the Contract abi
        self.supply_chain_abi = contract_interface['abi']

        # TRANSACTION BRIDGE CONTRACT
        # Getting the contract interface
        _, contract_interface = compiled_bridge.popitem()

        # Getting the Contract bytecode/bin
        self.bridge_bytecode = contract_interface['bin']
        # getting the Contract abi
        self.bridge_abi = contract_interface['abi']
        # DEPLOY SMART CONTRACT------------------------------------------------------
        # web3.py instance - Connectiong to Ganache App
        self.supply_chain_w3 = Web3(Web3.HTTPProvider(self.supply_chain_url))
        self.bridge_w3 = Web3(Web3.HTTPProvider(self.bridge_url))

        if self.supply_chain_w3.isConnected():
            print("[SUCCESS] Connected to the Supply Chain Ganache Blockchain Environment!")

        if self.bridge_w3.isConnected():
            print("[SUCCESS] Connected to the Transaction Bridge Ganache Blockchain Environment!")

        # Set first address as deployer for contract
        self.supply_chain_w3.eth.default_account = self.supply_chain_w3.eth.accounts[0]
        self.bridge_w3.eth.default_account = self.bridge_w3.eth.accounts[0]

        # Start deploying smart contract
        # Supply Chain
        print("[DEPLOYING] Deploying Supply Chain Contract...")

        SupplyChainContract = self.supply_chain_w3.eth.contract(abi = self.supply_chain_abi, bytecode = self.supply_chain_bytecode)

        # Submit transaction to deploy the contract then wait for receipt
        tx_hash = SupplyChainContract.constructor().transact()
        tx_receipt_supply = self.supply_chain_w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print("[SUCCESS] Supply Chain Contract Deployed!")

        # Transaction Bridge
        print("[DEPLOYING] Deploying Transaction Bridge Contract...")

        TransactionBridgeContract = self.bridge_w3.eth.contract(abi = self.bridge_abi, bytecode = self.bridge_bytecode)

        # Submit transaction to deploy the contract then wait for receipt
        tx_hash = TransactionBridgeContract.constructor().transact()
        tx_receipt_bridge = self.bridge_w3.eth.wait_for_transaction_receipt(tx_hash)
        
        self.supply_chain_address = tx_receipt_supply.contractAddress
        self.bridge_address = tx_receipt_bridge.contractAddress

        print("[SUCCESS] Transaction Bridge Contract Deployed!")
        # SAVE CONTRACT INFO-----------------------------------------------------
        # Supply Chain
        print("Saving Supply Chain Contract Info")

        with open('contracts/SupplyChain.info', "w") as file_obj:
            file_obj.write(self.supply_chain_address),
            file_obj.write("\n")
            file_obj.write(json.dumps(self.supply_chain_abi))
        print('[SUCCESS] Supply Chain info saved!')

        self.supply_chain_contract = self.supply_chain_w3.eth.contract(
            address = self.supply_chain_address,
            abi = self.supply_chain_abi
        )

        print('[SUCCESS] Supply Chain Contract Deployed Successfully!!!')

        # Transaction Bridge
        print("Saving Transaction Bridge Contract Info")

        with open('contracts/TransactionBridge.info', "w") as file_obj:
            file_obj.write(self.bridge_address),
            file_obj.write("\n")
            file_obj.write(json.dumps(self.bridge_abi))
        print('[SUCCESS] Supply Chain info saved!')

        self.bridge_contract = self.bridge_w3.eth.contract(
            address = self.bridge_address,
            abi = self.bridge_abi
        )
        print('[SUCCESS] Transaction Bridge Contract Deployed Successfully!!!')
        
    def connect(self) -> None:
        "A method to connect to already deployed System"
        # Connect to the web3 instances
        if self.supply_chain_w3 == None:
            self.supply_chain_w3 = Web3(Web3.HTTPProvider(self.supply_chain_url))
        if self.bridge_w3 == None:
            self.bridge_w3 = Web3(Web3.HTTPProvider(self.bridge_url))
        
        if self.supply_chain_w3.isConnected() and self.bridge_w3.isConnected():
            print("[SUCCESS] Connected to Supply Chain and Transaction Bridge Networks!")
        else:
            print("[ERROR] Cannot connect to one of the Networks...")
            exit()
        
        # Get contract info
        with open('contracts/SupplyChain.info', 'r') as file_obj:
            contract_info = file_obj.readlines()
            self.supply_chain_address = contract_info[0][:-1]
            self.supply_chain_abi = json.loads(contract_info[1])
        with open('contracts/TransactionBridge.info', 'r') as file_obj:
            contract_info = file_obj.readlines()
            self.bridge_address = contract_info[0][:-1]
            self.bridge_abi = json.loads(contract_info[1])
            
        # Set default accounts
        self.supply_chain_w3.eth.default_account = self.supply_chain_w3.eth.accounts[0]
        self.bridge_w3.eth.default_account = self.bridge_w3.eth.accounts[0]
        
        # Connect to contracts
        self.supply_chain_contract = self.supply_chain_w3.eth.contract(
            address = self.supply_chain_address,
            abi = self.supply_chain_abi
        )
        self.bridge_contract = self.bridge_w3.eth.contract(
            address = self.bridge_address,
            abi = self.bridge_abi
        )
        print("[SUCCESS] Connected to Supply Chain / Transaction Bridge Smart Contracts!")
    
    def is_connected(self) -> bool:
        """Method used to check if we are connected to the Ganache Apps.
        Returns True when connected.
        Returns False if contract not deployed or connected"""
        if self.supply_chain_w3 == None or self.bridge_w3 == None:
            print("[ERROR] Please deploy the system or connect to already deployed contract.")
            return False
        if not (self.supply_chain_w3.isConnected() and self.bridge_w3.isConnected()):
            print("[ERROR] Cannot connect to Blockchain Network!")
            return False
        if self.supply_chain_contract == None or self.bridge_contract == None:
            print("[ERROR] Please Connect to Smart Contract.")
            return False
        return True
    
    @staticmethod
    def print_instructions():
        "Prints the legends necessary to interact with smart contracts"
        print("""The following is the legend which is used to interact with the supply chain contract:
              \rApparel: Shirt-> 1, T-Shirt-> 2, Pants-> 3
              \rFabric: Cotton-> 1, Polyester-> 2
              \rBuy Items: [Cotton Shirt, Polyester Shirt, Cotton T-Shirt, Polyester T-Shirt, Cotton Pants, Polyester Pants]""")
    
    def buy_items(self, buy_list: List[int]) -> bool:
        """Buy items based on a list of 6 integers indicating how many of each item you want to get.\n
        Argument: List of integers indicating the number of each item you want to buy\n
        [Cotton Shirt, Polyester Shirt, Cotton T-Shirt, Polyester T-Shirt, Cotton Pants, Polyester Pants]"""
        # Error Checking
        if not self.is_connected():
            return False
        if len(buy_list) != 6:
            print("[ERROR] Argument must be a list of exactly 6 integers!")
            return False
        for item in buy_list:
            if type(item) != int:
                print("[ERROR] Item in argument was not an integer!")
                return False
        
        # Get user account input
        try:
            acc = int(input("Please enter the Account you want to buy from [1-9]: "))
            acc = self.supply_chain_w3.eth.accounts[acc]
        except Exception:
            print("[ERROR] Invalid Account Number!\n")
            return False
        
        # Send Transaction
        try:
            tx_hash = self.supply_chain_contract.functions.buy_product(buy_list).transact({'from': acc})
            tx_receipt = self.supply_chain_w3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception:
            print("[ERROR] Transaction Failed!")
            return False
        return True
        
    def get_product_info(self, apparel: int, fabric: int) -> Tuple:
        """Gets information about each product in the Supply Chain.\n
        returns: name, manufacturer, department, weight in grams, price in US cents, number left in stock\n
        returns: None if an error occurs."""
        if not self.is_connected():
            return None
        if type(apparel) != int or type(fabric) != int:
            print("[ERROR] Arguments are not integers!")
            return None
        return self.supply_chain_contract.functions.inquire_product(apparel, fabric).call()
    
    def change_item_info(self, apparel: int, fabric: int, price: int, weight: int) -> bool:
        """This function can only be used by the admin.\n
        Changes the price and weight of a particular item in Supply Chain.\n
        Price: US Cents, Weight: grams\n
        returns 'True' if transaction was successful otherwise returns 'False'"""
        # Error Checking
        if not self.is_connected():
            return False
        if type(apparel) != int or type(fabric) != int or type(price) != int or type(weight) != int:
            print("[ERROR] Arguments are not integers!")
            return False
        # Send Transaction
        try:
            tx_hash = self.supply_chain_contract.functions.change_clothes(
                apparel,
                fabric,
                price,
                weight
            ).transact({'from': self.supply_chain_w3.eth.accounts[0]})
            tx_receipt = self.supply_chain_w3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception:
            print("[ERROR] Transaction Failed!")
            return False
        return True
    
    def add_product(self, apparel: int, fabric: int, num_items: int) -> bool:
        """To be used by the Admin of the supply chain.\n
        Adds 'num_items' number of items to the particular apparel\n
        returns 'True' if transaction was successful otherwise returns 'False'"""
        # Error Checking
        if not self.is_connected():
            return False
        if type(apparel) != int or type(fabric) != int or type(num_items) != int:
            print("[ERROR] Arguments are not integers!")
            return False
        # Send Transaction
        try:
            tx_hash = self.supply_chain_contract.functions.add_products(
                apparel,
                fabric,
                num_items
            ).transact({'from': self.supply_chain_w3.eth.accounts[0]})
            tx_receipt = self.supply_chain_w3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception:
            print("[ERROR] Transaction Failed!")
            return False
        return True
    
    def defective_products(self, defective_list: List[int]) -> bool:
        """"""
        # Error Checking
        if not self.is_connected():
            return False
        if len(defective_list) != 6:
            print("[ERROR] Argument must be a list of 6 integers!")
            return False
        for item in defective_list:
            if type(item) != int:
                print("[ERROR] Items in argument must be integers!")
                return False
        # Send Transaction
        try:
            tx_hash = self.supply_chain_contract.functions.defective_products(
                defective_list
            ).transact({'from': self.supply_chain_w3.eth.accounts[0]})
            tx_receipt = self.supply_chain_w3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception:
            print("[ERROR] Transaction Failed!")
            return False
        return True
    
    