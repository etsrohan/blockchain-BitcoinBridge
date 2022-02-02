"""
This file is used to store different functions that will be useful to the functionality
of the Bitcoin Bridge system.
"""
import os
import json
from solcx import compile_source


class BitcoinBridgeGanache:
    """This class contains several methods and variables that help in the following functionality
    for the Bitcoin Bridge Blockchain Project.
    1) Deploy Smart Contracts: """
    
    def __init__(self):
        # Instance Variables
        supply_chain_address = None
        supply_chain_abi = None
        bridge_address = None
        bridge_abi = None
        
    def deploy_contracts(self, ganache_url1: str, ganache_url2: str):
        with open("contracts/SupplyChain.sol", "r") as file_object:
            compiled_supply = compile_source(file_object.read())
        
        print(compiled_supply)