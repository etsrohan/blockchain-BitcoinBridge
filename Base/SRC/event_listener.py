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
    print("\n[SUCCESS] Connected to the Ganache Blockchain Environment!")
    
# Getting smart conract information
with open('Contracts/SupplyChain.info', 'r') as file_object:
    contract_info = file_object.readlines()

supply_address = contract_info[0][:-1]
abi = json.loads(contract_info[1])

# Set first address as deployer for contract
w3.eth.default_account = w3.eth.accounts[0]

# Start deploying smart contract
print("\n[CONNECTING] Connecting to Supply Chain Contract...")

supplychain = w3.eth.contract(
    address = supply_address,
    abi = abi
)
print("\n[SUCCESS] Connected to Supply Chain Smart Contract...")
# -----------------------------MAIN PROGRAM-----------------------------
# event NewDeliveryCreated (uint256 indexed delivery_id, address employee_address, string supplier, MaterialType material);
# event DeliveryCreationFailed (string supplier, uint8 material, uint256 weight, uint256 cost, string message);
# event NewBatchCreated (uint256 indexed batch_id, address employee_address, BatchType fabric, ItemType apparel);
# event BatchCreationFailed (uint8 fabric, uint256 machine_id, string message);
# event BatchCompletionFailed (uint256 indexed batch_id, string message);
# event BatchCompleted (uint256 indexed batch_id, uint256 num_items);
# event DeliveryReceived (uint256 indexed delivery_id);
# event DeliveryCancelled( uint256 indexed delivery_id);
# event NewItemsCreated (uint256 indexed item_start_id, uint256 indexed item_end_id, BatchType fabric, ItemType item_type);
# event ItemSold (uint256 indexed item_id, uint256 indexed receipt_num, uint256 date);
# event ItemReturned (uint256 indexed item_id, uint256 indexed receipt_num, uint256 date, uint256 price);

# EVENT HANDLING FUNCTIONS
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
                ir_loop(ir_filter, 2)
                
            )
        )
    except KeyboardInterrupt as err:
        print('\nClosing event listener...')
        print(err)
    finally:
        loop.close()

if __name__ == '__main__':
    main()