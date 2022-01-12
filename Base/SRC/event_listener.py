from web3 import Web3
import threading
import json
import asyncio
import time

# ---------------------CONNECT TO SUPPLY CHAIN CONTRACT ON GANACHE---------------------
# web3.py instance - Connectiong to Ganache App
GANACHE_URL = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if w3.isConnected():
    print("\n[SUCCESS] Connected to the Supply Chain Ganache Blockchain Environment!")
    
GANACHE_URL2 = "HTTP://127.0.0.1:7546"
w32 = Web3(Web3.HTTPProvider(GANACHE_URL2))

if w32.isConnected():
    print("\n[SUCCESS] Connected to the Transaction Bridge Ganache Blockchain Environment!")
    
# Getting SC smart contract information
with open('Contracts/SupplyChain.info', 'r') as file_object:
    contract_info = file_object.readlines()

supply_address = contract_info[0][:-1]
supply_abi = json.loads(contract_info[1])

# Getting TB smart contract information
with open('Contracts/TransactionBridge.info', 'r') as file_object:
    contract_info = file_object.readlines()

bridge_address = contract_info[0][:-1]
bridge_abi = json.loads(contract_info[1])

# Set first address as deployer for contract
w3.eth.default_account = w3.eth.accounts[0]
w32.eth.default_account = w32.eth.accounts[0]

# Start connecting to smart contracts
print("\n[CONNECTING] Connecting to Supply Chain Contract...")

supplychain = w3.eth.contract(
    address = supply_address,
    abi = supply_abi
)
print("\n[SUCCESS] Connected to Supply Chain Smart Contract...")

print("\n[CONNECTING] Connecting to Transaction Bridge Contract...")

transactionbridge = w32.eth.contract(
    address = bridge_address,
    abi = bridge_abi
)
print("\n[SUCCESS] Connected to Transaction Bridge Smart Contract...")
# -----------------------------MAIN PROGRAM-----------------------------
print("\nListnening for new events...\n")
# A dictionary to store the transaction_id for every receipt number
trans_dict = {}

# EVENT HANDLING FUNCTIONS
def transaction_created(transaction_id, receipt_number):
    """
    A target function to handle the event of a transaction being 
    created on transaction bridge.
    """
    print(
        f"""\nShopping Cart Created:
            \r\tTransaction ID: {transaction_id}
            \r\tReceipt Number: {receipt_number}"""
    )

def transaction_updated(transaction_id, receipt_number, total):
    """
    A target function to handle the event of a transaction being 
    updated on transaction bridge.
    """
    print(
        f"""\nShopping Cart Updated:
            \r\tTransaction ID: {transaction_id}
            \r\tReceipt Number: {receipt_number}
            \r\tNew Total Amount Due: ${total / 100}"""
    )

def transaction_refunded(transaction_id, receipt_number):
    """
    A target function to handle the event of a transaction being 
    refunded on transaction bridge.
    """
    print(
        f"""\Transaction Refunded:
            \r\tTransaction ID: {transaction_id}
            \r\tReceipt Number: {receipt_number}"""
    )

def payment_initiated(transaction_id, receipt_number, total):
    """
    A target function to handle the event of a payment being 
    initiated on transaction bridge.
    """
    print(
        f"""\nPayment Process Initiated:
            \r\tTransaction ID: {transaction_id}
            \r\tReceipt Number: {receipt_number}
            \r\tTotal Amount Due: ${total / 100}"""
    )

def new_delivery_created(delivery_id, employee_address, supplier, material):
    """
    A target function to handle the event of a delivery order
    created by the manufacturing plant.
    """
    print(
        f"""\nDelivery Order Created:
            \r\tDelivery ID: {delivery_id}
            \r\tEmployee Address: {employee_address}
            \r\tSupplier: {supplier}
            \r\tMaterial Type: {material}"""
    )

def delivery_creation_failed(supplier, material, weight, cost, message):
    """
    A target function to handle the event of a a delovery order
    failed by the manufacturing plant.
    """
    print(
        f"""\nDelivery Creation Failed:
            \r\tSupplier: {supplier}
            \r\tMaterial Type: {material}
            \r\tWeight of Materials: {weight}
            \r\tCost of Materials:: {cost}
            \r\tError Message: {message}"""
    )

def new_batch_created(batch_id, employee_address, fabric, apparel):
    """
    A target function to handle the event of a new batch being
    created by the manufacturing plant.
    """
    print(
        f"""\nNew Batch Created:
            \r\tBatch ID: {batch_id}
            \r\tEmployee Address: {employee_address}
            \r\tFabric Type: {fabric}
            \r\tApparel Type: {apparel}"""
    )

def batch_creation_failed(fabric, machine_id, message):
    """
    A target function to handle the event of a batch creation
    failed by the manufacturing plant.
    """
    print(
        f"""\nBatch Creation Failed:
            \r\tBatch Fabric: {fabric}
            \r\tMachine ID: {machine_id}
            \r\tError Message: {message}"""
    )

def batch_completion_failed(batch_id, message):
    """
    A target function to handle the event of a batch
    completion failed by the manufacturing plant.
    """
    print(
        f"""\nBatch Completion Failed:
            \r\tBatch ID: {batch_id}
            \r\tError Message: {message}"""
    )

def batch_completed(batch_id, num_items):
    """
    A target function to handle the event of a batch being
    completed by the manufacturing plant.
    """
    print(
        f"""\nBatch Completed:
            \r\tBatch ID: {batch_id}
            \r\tNumber of Items: {num_items}"""
    )

def delivery_received(delivery_id):
    """
    A target function to handle the event of a delivery being 
    received by a company
    """
    print(
        f"""\nDelivery Received:
            \r\tDelivery ID: {delivery_id}"""
    )

def delivery_cancelled(delivery_id):
    """
    A target function to handle the event of a delivery being 
    cancelled by a company
    """
    print(
        f"""\nDelivery Cancelled:
            \r\tDelivery ID: {delivery_id}"""
    )

def new_items_created(item_start_id, item_end_id, fabric, item_type):
    """
    A target function to handle the event of items being created
    by a completed batch
    """
    print(
        f"""\nNew Items Created:
            \r\tItem Start ID: {item_start_id}
            \r\tItem End ID: {item_end_id}
            \r\tFabric Type: {fabric}
            \r\tItem Type: {item_type}"""
    )

def item_sold(item_id, receipt_number, date):
    """
    A target function to handle the event of an item being sold
    """
    print(
        f"""\nNew Item Sold:
            \r\tItem ID: {item_id}
            \r\tReceipt Number: {receipt_number}
            \r\tDate: {time.ctime(date)}"""
    )
    # Create a new transaction if receipt number is unique else
    # add item to existing cart (transaction)

def item_returned(item_id, receipt_number, date, price):
    """
    A target function to handle the event of an item being returned
    """
    print(
        f"""\nNew Item Returned:
            \r\tItem ID: {item_id}
            \r\tReceipt Number: {receipt_number}
            \r\tDate: {time.ctime(date)}
            \r\tPrice Refunded: ${price / 100}"""
    )

# ASYNC FUNCTION LOOPS
# TransactionCreated (uint256 indexed transaction_id, uint256 receipt_number);
async def tc_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every payment being
    processed.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = transaction_created,
                args = (
                    event['args']['transaction_id'],
                    event['args']['receipt_number']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# TransactionUpdated (uint256 indexed transaction_id, uint256 receipt_number, uint256 total);
async def tu_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every transaction being
    updated.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = transaction_updated,
                args = (
                    event['args']['transaction_id'],
                    event['args']['receipt_number'],
                    event['args']['total']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# TransactionRefunded (uint256 indexed transaction_id, uint256 receipt_number);
async def tr_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every transaction being
    refunded.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = transaction_refunded,
                args = (
                    event['args']['transaction_id'],
                    event['args']['receipt_number']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# PaymentInitiated (uint256 indexed transaction_id, uint256 receipt_number, uint256 total);
async def payment_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every payment being
    processed.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = payment_initiated,
                args = (
                    event['args']['transaction_id'],
                    event['args']['receipt_number'],
                    event['args']['total']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# NewDeliveryCreated (uint256 indexed delivery_id, address employee_address, string supplier, MaterialType material);
async def ndc_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every new delivery orders
    successfully created.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = new_delivery_created,
                args = (
                    event['args']['delivery_id'],
                    event['args']['employee_address'],
                    event['args']['supplier'],
                    event['args']['material']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# DeliveryCreationFailed (string supplier, uint8 material, uint256 weight, uint256 cost, string message);
async def dcf_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every new delivery order
    unsuccessfully created.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = delivery_creation_failed,
                args = (
                    event['args']['supplier'],
                    event['args']['material'],
                    event['args']['weight'],
                    event['args']['cost'],
                    event['args']['message']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# NewBatchCreated (uint256 indexed batch_id, address employee_address, BatchType fabric, ItemType apparel);
async def nbc_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every new batch
    created for completion by a manufacturing plant.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = new_batch_created,
                args = (
                    event['args']['batch_id'],
                    event['args']['employee_address'],
                    event['args']['fabric'],
                    event['args']['apparel']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# BatchCreationFailed (uint8 fabric, uint256 machine_id, string message);
async def bcrf_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every batch
    creation failed by a manufacturing plant.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = batch_creation_failed,
                args = (
                    event['args']['fabric'],
                    event['args']['machine_id'],
                    event['args']['message']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# BatchCompletionFailed (uint256 indexed batch_id, string message);
async def bcof_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every batch
    completion failed by a manufacturing plant.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = batch_completion_failed,
                args = (
                    event['args']['batch_id'],
                    event['args']['message']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# BatchCompleted (uint256 indexed batch_id, uint256 num_items);
async def bc_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every batch
    completed by a manufacturing plant.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = batch_completed,
                args = (
                    event['args']['batch_id'],
                    event['args']['num_items']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# DeliveryReceived (uint256 indexed delivery_id);
async def dr_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every delivery
    cancelled by a company.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = delivery_received,
                args = (
                    event['args']['delivery_id'],
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# DeliveryCancelled( uint256 indexed delivery_id);
async def dc_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every delivery
    cancelled by a company.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = delivery_cancelled,
                args = (
                    event['args']['delivery_id'],
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)
        
# ItemReturned (uint256 indexed item_id, uint256 indexed receipt_num, uint256 date, uint256 price);
async def ir_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every item
    returned by a customer.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = item_returned,
                args = (
                    event['args']['item_id'],
                    event['args']['receipt_num'],
                    event['args']['date'],
                    event['args']['price']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# ItemSold (uint256 indexed item_id, uint256 indexed receipt_num, uint256 date);
async def is_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every item
    sold to a customer.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = item_sold,
                args = (
                    event['args']['item_id'],
                    event['args']['receipt_num'],
                    event['args']['date']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# NewItemsCreated (uint256 indexed item_start_id, uint256 indexed item_end_id, BatchType fabric, ItemType item_type);
async def nic_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for new items created
    by a batch being completed.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = new_items_created,
                args = (
                    event['args']['item_start_id'],
                    event['args']['item_end_id'],
                    event['args']['fabric'],
                    event['args']['item_type']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# Main Function
def main():
    # Creating filters for every event
    ndc_filter = supplychain.events.NewDeliveryCreated().createFilter(fromBlock = 'latest')
    dcf_filter = supplychain.events.DeliveryCreationFailed().createFilter(fromBlock = 'latest')
    nbc_filter = supplychain.events.NewBatchCreated().createFilter(fromBlock = 'latest')
    bcrf_filter = supplychain.events.BatchCreationFailed().createFilter(fromBlock = 'latest')
    bcof_filter = supplychain.events.BatchCompletionFailed().createFilter(fromBlock = 'latest')
    bc_filter = supplychain.events.BatchCompleted().createFilter(fromBlock = 'latest')
    dr_filter = supplychain.events.DeliveryReceived().createFilter(fromBlock = 'latest')
    dc_filter = supplychain.events.DeliveryCancelled().createFilter(fromBlock = 'latest')
    nic_filter = supplychain.events.NewItemsCreated().createFilter(fromBlock = 'latest')
    is_filter = supplychain.events.ItemSold().createFilter(fromBlock = 'latest')
    ir_filter = supplychain.events.ItemReturned().createFilter(fromBlock = 'latest')
    tc_filter = transactionbridge.events.TransactionCreated().createFilter(fromBlock = 'latest')
    tu_filter = transactionbridge.events.TransactionUpdated().createFilter(fromBlock = 'latest')
    tr_filter = transactionbridge.events.TransactionRefunded().createFilter(fromBlock = 'latest')
    payment_filter = transactionbridge.events.PaymentInitiated().createFilter(fromBlock = 'latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                ndc_loop(ndc_filter, 2),
                dcf_loop(dcf_filter, 2),
                nbc_loop(nbc_filter, 2),
                bcrf_loop(bcrf_filter, 2),
                bcof_loop(bcof_filter, 2),
                bc_loop(bc_filter, 2),
                dr_loop(dr_filter, 2),
                dc_loop(dc_filter, 2),
                nic_loop(nic_filter, 2),
                is_loop(is_filter, 2),
                ir_loop(ir_filter, 2),
                tc_loop(tc_filter, 2),
                tu_loop(tu_filter, 2),
                tr_loop(tr_filter, 2),
                payment_loop(payment_filter, 2)
            )
        )
    except KeyboardInterrupt as err:
        print('\nClosing event listener...')
        print(err)
    finally:
        loop.close()

if __name__ == '__main__':
    main()