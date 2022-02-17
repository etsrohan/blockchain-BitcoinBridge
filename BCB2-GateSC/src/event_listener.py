import threading
import asyncio
import time
from functions.bcb_functions import BitcoinBridgeGanache
import random

# ---------------------CONNECT TO SUPPLY CHAIN CONTRACT ON GANACHE---------------------
# New instance of Bitcoin Bridge Class
bcb = BitcoinBridgeGanache()

bcb.connect()

pins_dict = {
    1: 'Six',
    2: 'Eight',
    3: 'Twelve',
    4: 'Fourteen'
}
gate_dict = {
    1: 'NAND',
    2: 'NOR'
}
receipts = set()
chips_tuple = (
    (1,1),
    (2,1),
    (1,2),
    (2,2),
    (1,3),
    (2,3),
    (1,4),
    (2,4),
)

# -----------------------------MAIN PROGRAM-----------------------------
print("\nListnening for new events...\n")

# EVENT HANDLING FUNCTIONS
def products_added(gate, pins, num_added):
    """A function to handle the event of new products being added"""
    print(f"""\nNew Product was added:
          \r\tItem:{gate_dict[gate]}-{pins_dict[pins]}\tNumber: {num_added}""")
    

def bought_items(num_buy):
    """A function to handle the event of particular items being bought."""
    # Getting random receipt number
    receipt_number = random.randint(1,999999)
    while receipt_number in receipts:
        receipt_number = random.randint(1,999999)
    receipts.add(receipt_number)
    
    item_id = [random.randint(1,100) for _ in range(8)]

    prices = [num_buy[index] * bcb.get_product_info(gate, pins)[3] for index, (gate, pins) in enumerate(chips_tuple)]
    
    
    for index, (gate, pins) in enumerate(chips_tuple):
        if len(f"{gate_dict[gate]}-{pins_dict[pins]}") > 10:
            print(f"Item:{gate_dict[gate]}-{pins_dict[pins]}\tNumber: {num_buy[index]}\tPrice: ${prices[index]/100}")
        else:
            print(f"Item:{gate_dict[gate]}-{pins_dict[pins]}\t\tNumber: {num_buy[index]}\tPrice: ${prices[index]/100}")
    
    bcb.create_basket(receipt_number)
    
    bcb.add_items_to_basket(receipt_number, item_id, prices)

def defective_items(num_defective):
    """A function to handle the event of removing defective items from the supply chain."""
    print(f"""Removing the following items from the supply chain.""")
    for index, (gate, pins) in enumerate(chips_tuple):
        print(f"Item:{gate_dict[gate]}-{pins_dict[pins]}\tNumber: {num_defective[index]}")

def transaction_created(receipt_number):
    """
    A target function to handle the event of a transaction being 
    created on transaction bridge.
    """
    print(
        f"""\nShopping Cart Created:
            \r\tReceipt Number: {receipt_number}"""
    )

def transaction_updated(receipt_number, total):
    """
    A target function to handle the event of a transaction being 
    updated on transaction bridge.
    """
    print(
        f"""\nShopping Cart Updated:
            \r\tReceipt Number: {receipt_number}
            \r\tNew Total Amount Due: ${total / 100}"""
    )

def transaction_refunded(receipt_number, total):
    """
    A target function to handle the event of a transaction being 
    refunded on transaction bridge.
    """
    print(
        f"""\Transaction Refunded:
            \r\tReceipt Number: {receipt_number}
            \r\tRefund Amount: ${total/100}"""
    )
    
    # Send refund amount on BTC Network
    print("Sending Bitcoin Transaction as refund...")
    bcb.send_btc(total, reverse = True)

def payment_initiated(receipt_number, total):
    """
    A target function to handle the event of a payment being 
    initiated on transaction bridge.
    """
    print(
        f"""\nPayment Process Initiated:
            \r\tReceipt Number: {receipt_number}
            \r\tTotal Amount Due: ${total / 100}"""
    )
    # Send BTC Transaction
    print("Sending Bitcoin Transaction as payment...")
    
    bcb.send_btc(total)
  
def seller_ok(receipt_number, total):
    """
    A target function to handle the event of a seller confirming transaction
    """
    print(f"""\nSeller has confirmed the transaction.
          \rReceipt Number: {receipt_number}
          \rTotal: ${total/100}""")

def buyer_ok(receipt_number, total):
    """
    A target function to handle the event of a buyer confirming transaction
    """
    print(f"""\nBuyer has confirmed the transaction.
          \rReceipt Number: {receipt_number}
          \rTotal: ${total/100}""")

# ASYNC FUNCTION LOOPS
# event items_defective(uint256[8] num_defective);
async def id_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every defective item removed from
    the supply chain.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = defective_items,
                args = (
                    event['args']['num_defective'],
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# event items_bought(uint256[8] num_buy);
async def ib_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every bunch of items bought 
    in supply chain.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = bought_items,
                args = (
                    event['args']['num_buy'],
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# event added_products(GateType indexed gate, NumPins indexed pins, uint256 num_added);
async def ap_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every item added in  
    supply chain.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = products_added,
                args = (
                    event['args']['gate'],
                    event['args']['pins'],
                    event['args']['num_added']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# event SellerOk (uint256 indexed receipt_number, uint256 total);
async def sellerok_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every seller confirming the 
    transaction.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = seller_ok,
                args = (
                    event['args']['receipt_number'],
                    event['args']['total']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# event BuyerOk (uint256 indexed receipt_number, uint256 total);
async def buyerok_loop(event_filter, poll_interval):
    """
    Asynchronous function to create new threads for every buyer confirming the 
    transaction.
    """
    
    while True:
        for event in event_filter.get_new_entries():
            thread = threading.Thread(
                target = buyer_ok,
                args = (
                    event['args']['receipt_number'],
                    event['args']['total']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# TransactionCreated (uint256 indexed receipt_number);
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
                    event['args']['receipt_number'],
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# TransactionUpdated (uint256 indexed receipt_number, uint256 total);
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
                    event['args']['receipt_number'],
                    event['args']['total']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# TransactionRefunded (uint256 indexed receipt_number);
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
                    event['args']['receipt_number'],
                    event['args']['total']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# PaymentInitiated (uint256 indexed receipt_number, uint256 total);
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
                    event['args']['receipt_number'],
                    event['args']['total']
                )
            )
            thread.start()
        await asyncio.sleep(poll_interval)

# Main Function
def main():
    # Creating filters for every event
    ap_filter = bcb.supply_chain_contract.events.added_products().createFilter(fromBlock = 'latest')
    ib_filter = bcb.supply_chain_contract.events.items_bought().createFilter(fromBlock = 'latest')
    id_filter = bcb.supply_chain_contract.events.items_defective().createFilter(fromBlock = 'latest')
    tc_filter = bcb.bridge_contract.events.TransactionCreated().createFilter(fromBlock = 'latest')
    tu_filter = bcb.bridge_contract.events.TransactionUpdated().createFilter(fromBlock = 'latest')
    tr_filter = bcb.bridge_contract.events.TransactionRefunded().createFilter(fromBlock = 'latest')
    payment_filter = bcb.bridge_contract.events.PaymentInitiated().createFilter(fromBlock = 'latest')
    sellerok_filter = bcb.bridge_contract.events.SellerOk().createFilter(fromBlock = 'latest')
    buyerok_filter = bcb.bridge_contract.events.BuyerOk().createFilter(fromBlock = 'latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                ap_loop(ap_filter, 2),
                ib_loop(ib_filter, 2),
                id_loop(id_filter, 2),
                tc_loop(tc_filter, 2),
                tu_loop(tu_filter, 2),
                tr_loop(tr_filter, 2),
                payment_loop(payment_filter, 2),
                sellerok_loop(sellerok_filter, 2),
                buyerok_loop(buyerok_filter, 2)
            )
        )
    except KeyboardInterrupt as err:
        print('\nClosing event listener...')
        print(err)
    finally:
        loop.close()

if __name__ == '__main__':
    main()