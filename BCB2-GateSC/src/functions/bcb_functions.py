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
    # Class Variables
    SUPPLY_CHAIN_URL = "HTTP://127.0.0.1:7545"
    BRIDGE_URL = "HTTP://127.0.0.1:7546"
    
    def __init__(self):
        # Instance Variables
        # SUPPLY CHAIN
        self.supply_chain_address = None
        self.supply_chain_abi = None
        self.supply_chain_bytecode = None
        self.supply_chain_w3 = None
        self.supply_chain_contract = None
        # BRIDGE
        self.bridge_address = None
        self.bridge_abi = None
        self.bridge_bytecode = None
        self.bridge_w3 = None
        self.bridge_contract = None
        # BITCOIN
        self.btc_seller = None
        self.btc_buyer = None
        
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
        # DEPLOY SMART CONTRACT
        # web3.py instance - Connectiong to Ganache App
        self.supply_chain_w3 = Web3(Web3.HTTPProvider(self.SUPPLY_CHAIN_URL))
        self.bridge_w3 = Web3(Web3.HTTPProvider(self.BRIDGE_URL))

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
        # SAVE CONTRACT INFO
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
        
        # BITCOIN TESTNET
        with open("wallet/wallet.info", 'r') as file_object:
            accs = file_object.readlines()
            accs[0] = accs[0][:-1]
        self.buyer = PrivateKeyTestnet(accs[0])
        self.seller = PrivateKeyTestnet(accs[1])
        print('[SUCCESS] Connected to Bitcoin Testnet!')
        
        
    def connect(self) -> None:
        "A method to connect to already deployed System"
        # Connect to the web3 instances
        if self.supply_chain_w3 == None:
            self.supply_chain_w3 = Web3(Web3.HTTPProvider(self.SUPPLY_CHAIN_URL))
        if self.bridge_w3 == None:
            self.bridge_w3 = Web3(Web3.HTTPProvider(self.BRIDGE_URL))
        
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
        # BITCOIN TESTNET
        with open("wallet/wallet.info", 'r') as file_object:
            accs = file_object.readlines()
            accs[0] = accs[0][:-1]
        self.buyer = PrivateKeyTestnet(accs[0])
        self.seller = PrivateKeyTestnet(accs[1])
        print('[SUCCESS] Connected to Bitcoin Testnet!')
    
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
        print("""\nThe following is the legend which is used to interact with the supply chain contract:
              \rNumber of Pins: Six-> 1, Eight-> 2, Twelve-> 3, Fourteen-> 4
              \rGate Type: NAND-> 1, NOR-> 2
              \rThe option to buy chips is ordered in the following manner
              \rBuy Items: [NAND-6, NOR-6, NAND-8, NOR-8, NAND-12, NOR-12, NAND-14, NOR-14]\n""")
    
    
    # SUPPLY CHAIN CONTRACT METHODS--------------------------------------------------
    def buy_items(self, buy_list: List[int]) -> bool:
        """Buy items based on a list of 8 integers indicating how many of each item you want to get.\n
        Argument: List of integers indicating the number of each item you want to buy\n
        [NAND-6, NOR-6, NAND-8, NOR-8, NAND-12, NOR-12, NAND-14, NOR-14]\n
        returns 'True' if transaction was successful otherwise returns 'False'"""
        # Error Checking
        if not self.is_connected():
            return False
        if len(buy_list) != 8:
            print("[ERROR] Argument must be a list of exactly 8 integers!")
            return False
        for item in buy_list:
            if type(item) != int:
                print("[ERROR] Item in argument was not an integer!")
                return False
        
        acc = self.supply_chain_w3.eth.accounts[1]
        
        # Send Transaction
        try:
            tx_hash = self.supply_chain_contract.functions.buy_product(buy_list).transact({'from': acc})
            tx_receipt = self.supply_chain_w3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception:
            print("[ERROR] Transaction Failed!")
            return False
        return True
        
    def get_product_info(self, gate: int, pins: int) -> Tuple:
        """Gets information about each product in the Supply Chain.\n
        returns: name, manufacturer, department, price in US cents, input voltage, number left in stock,
        number of gates in chip\n
        returns: None if an error occurs."""
        if not self.is_connected():
            return None
        if type(gate) != int or type(pins) != int:
            print("[ERROR] Arguments are not integers!")
            return None
        return self.supply_chain_contract.functions.inquire_product(gate, pins).call()
    
    def change_item_info(self, gate: int, pins: int, price: int, voltage: int) -> bool:
        """This function can only be used by the admin.\n
        Changes the price and voltage of a particular item in Supply Chain.\n
        Price: US Cents, Voltage: millivolts\n
        returns 'True' if transaction was successful otherwise returns 'False'"""
        # Error Checking
        if not self.is_connected():
            return False
        if type(gate) != int or type(pins) != int or type(price) != int or type(voltage) != int:
            print("[ERROR] Arguments are not integers!")
            return False
        # Send Transaction
        try:
            tx_hash = self.supply_chain_contract.functions.change_properties(
                gate,
                pins,
                price,
                voltage
            ).transact({'from': self.supply_chain_w3.eth.accounts[0]})
            tx_receipt = self.supply_chain_w3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception:
            print("[ERROR] Transaction Failed!")
            return False
        return True
    
    def add_product(self, gate: int, pins: int, num_items: int) -> bool:
        """To be used by the Admin of the supply chain.\n
        Adds 'num_items' number of items to the chip type\n
        returns 'True' if transaction was successful otherwise returns 'False'"""
        # Error Checking
        if not self.is_connected():
            return False
        if type(gate) != int or type(pins) != int or type(num_items) != int:
            print("[ERROR] Arguments are not integers!")
            return False
        # Send Transaction
        try:
            tx_hash = self.supply_chain_contract.functions.add_products(
                gate,
                pins,
                num_items
            ).transact({'from': self.supply_chain_w3.eth.accounts[0]})
            tx_receipt = self.supply_chain_w3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception:
            print("[ERROR] Transaction Failed!")
            return False
        return True
    
    def defective_products(self, defective_list: List[int]) -> bool:
        """A method to be used by the admin of supply chain contract.\n
        A method used to remove defective products from the supply chain.\n
        argument: defective_list is a list of 8 integers that are the number of each corresponding item below.\n
        [NAND-6, NOR-6, NAND-8, NOR-8, NAND-12, NOR-12, NAND-14, NOR-14]\n
        returns 'True' if transaction was successful otherwise returns 'False'"""
        # Error Checking
        if not self.is_connected():
            return False
        if len(defective_list) != 8:
            print("[ERROR] Argument must be a list of 8 integers!")
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
    # ---------------------------------------------------------------------------------
    
    # BRIDGE CONTRACT METHODS----------------------------------------------------------
    def create_basket(self, receipt_number: int) -> bool:
        """Create a new transaction to get total of all items in the basket.\n
        arguments: receipt_number is the receipt number of basket to be paid with bitcoin.\n
        returns 'True' if transaction was successful otherwise returns 'False'"""
        # Error Checking
        if not self.is_connected():
            return False
        if type(receipt_number) != int:
            print("[ERROR] Receipt Number must be an integer!")
            return False
        # Send Transaction
        try:
            tx_hash = self.bridge_contract.functions.create_transaction(
                receipt_number
            ).transact({'from': self.bridge_w3.eth.accounts[0]})
            tx_receipt = self.bridge_w3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception:
            print("[ERROR] Transaction Failed!")
            return False
        return True
    
    def add_items_to_basket(self, receipt_number: int, items: List[int], prices: List[int]) -> bool:
        """Add particular items to the basket to be ready for payment.\n
        Arguments:\n
        \treceipt_num -> integer representing the receipt number of basket\n
        \titems -> A list of item numbers to be added to basket\n
        \tprices -> A list of prices in cents used to calculate new total for whole basket.\n
        returns 'True' if transaction was successful otherwise returns 'False'"""
        # Error Checking
        if not self.is_connected():
            return False
        if type(receipt_number) != int:
            print("[ERROR] Receipt Number must be an integer!")
            return False
        if len(items) != len(prices):
            print("[ERROR] Number of items does not match number of prices!")
            return False
        for index in range(len(items)):
            if type(items[index]) != int or type(prices[index]) != int:
                print("[ERROR] Arguments 'items' and 'prices' must contain only integers!")
                return False
        # Send Transaction
        try:
            tx_hash = self.bridge_contract.functions.add_items_to_transaction(
                receipt_number,
                items,
                prices
            ).transact({'from': self.bridge_w3.eth.accounts[0]})
            tx_receipt = self.bridge_w3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception:
            print("[ERROR] Transaction Failed!")
            return False
        return True
    
    def seller_confirmation(self, receipt_number: int, seller_address: str) -> bool:
        """Method to get confirmation from the seller to proceed with payment\n
        returns 'True' if transaction was successful otherwise returns 'False'"""
        # Error Checking
        if not self.is_connected():
            return False
        if type(receipt_number) != int:
            print("[ERROR] Receipt Number must be an integer!")
            return False
        # Send Transaction
        try:
            tx_hash = self.bridge_contract.functions.confirm_seller(
                receipt_number
            ).transact({'from': seller_address})
            tx_receipt = self.bridge_w3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception:
            print("[ERROR] Transaction Failed! Please check Receipt Number to see if it is valid!")
            return False
        return True
    
    def buyer_confirmation(self, receipt_number: int, buyer_address: str) -> bool:
        """Method to get confirmation from the buyer to proceed with payment\n
        returns 'True' if transaction was successful otherwise returns 'False'"""
        # Error Checking
        if not self.is_connected():
            return False
        if type(receipt_number) != int:
            print("[ERROR] Receipt Number must be an integer!")
            return False
        # Send Transaction
        try:
            tx_hash = self.bridge_contract.functions.confirm_buyer(
                receipt_number
            ).transact({'from': buyer_address})
            tx_receipt = self.bridge_w3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception:
            print("[ERROR] Transaction Failed! Please check Receipt Number to see if it is valid!")
            return False
        return True
    
    def pay_basket(self, receipt_number: int) -> bool:
        """A method to initiate the payment process for a receipt number.\n
        This method only succeeds after both the seller and the buyer have sent their
        confirmations for payment.\n
        returns 'True' if transaction was successful otherwise returns 'False'"""
        # Error Checking
        if not self.is_connected():
            return False
        if type(receipt_number) != int:
            print("[ERROR] Receipt Number must be an integer!")
            return False
        # Send Transaction
        try:
            tx_hash = self.bridge_contract.functions.pay_transaction(
                receipt_number
            ).transact({'from': self.bridge_w3.eth.accounts[0]})
            tx_receipt = self.bridge_w3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception:
            print("[ERROR] Transaction Failed! Please enter a valid receipt number or check to see if transaction is already paid.")
            return False
        return True
    
    def refund_basket(self, receipt_number: int) -> bool:
        """A method to initiate the refund process for a receipt number.\n
        This method only succeeds after a payment has been successfully been processed.\n
        returns 'True' if transaction was successful otherwise returns 'False'"""
        # Error Checking
        if not self.is_connected():
            return False
        if type(receipt_number) != int:
            print("[ERROR] Receipt Number must be an integer!")
            return False
        # Send Transaction
        try:
            tx_hash = self.bridge_contract.functions.refund_transaction(
                receipt_number
            ).transact({'from': self.bridge_w3.eth.accounts[0]})
            tx_receipt = self.bridge_w3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception:
            print("[ERROR] Transaction Failed! Please enter a valid receipt number or check to see if transaction failed or is already refunded.")
            return False
        return True
    
    def get_basket_state(self, receipt_number: int) -> int:
        """Gets state of the basket with associated receipt number\n
        return value: 0 -> Not Created, 1 -> Created, 2 -> Completed, 3 -> Failed, 4 -> Refunded"""
        # Error Checking
        if not self.is_connected():
            return None
        if type(receipt_number) != int:
            print("[ERROR] Receipt Number must be an integer!")
            return None
        return self.bridge_contract.functions.get_state(receipt_number).call()
    
    def get_num_baskets(self) -> int:
        """Gets the number of baskets made by the TransactionBridge Contract."""
        # Error Checking
        if not self.is_connected():
            return None
        return self.bridge_contract.functions.get_num_trans().call()
    
    # ---------------------------------------------------------------------------------
    
    # BITCOIN METHODS------------------------------------------------------------------
    def get_balance_btc(self, currency: str) -> None:
        """Gets the buyer and seller balances in either usd or btc\n
        currency: 'usd' or 'btc'"""
        currency = currency.lower()
        if currency != 'usd' and currency != 'btc':
            print("[ERROR] Currency should be only 'btc' or 'usd'!")
            return
        
        print(f"""Current Balances [{currency}]\n
        \r\tBuyer:\tAddress: {self.buyer.address}\t{self.buyer.get_balance(currency)}\n
        \r\tSeller:\tAddress: {self.seller.address}\t{self.seller.get_balance(currency)}""")
    
    def send_btc(self, amount: int, reverse: bool = False) -> bool:
        """Sends 'amount', in US cents, worth of bitcoin from one account to another\n
        by default sends from buyer to seller\n
        if reverse = True then sends from seller to buyer.\n
        amount: amount to send in cents (USD)"""
        if type(amount) != int:
            print("[ERROR] 'Amount' should be an integer!")
            return False
        
        try:
            if not reverse:
                tx_hash = self.buyer.send([(self.seller.address, amount/100, 'usd')])
                print(tx_hash)
            else:
                tx_hash = self.seller.send([(self.buyer.address, amount/100, 'usd')])
                print(tx_hash)
        except Exception:
            print("[ERROR] Bitcoin transaction failed! Please try again!")
            return False
        return True
    
    # ---------------------------------------------------------------------------------
