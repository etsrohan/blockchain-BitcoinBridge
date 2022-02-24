from functions.bcb_functions import BitcoinBridgeGanache

bcb = BitcoinBridgeGanache()

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
    (2,4)
)

def main():
    print("""\n------------------------------------------------
    \rWelcome to the Bitcoin Bridge System Demo!
    \rPlease select from one of the following options:
    \r\t1.  [Admin] Deploy System
    \r\t2.  Connect to an already deployed system
    \r\t3.  Instructions
    \r\t4.  Get Product Information
    \r\t5.  Add Products to Cart
    \r\t6.  [Admin] Change Item Information
    \r\t7.  [Admin] Add more Items in Supply Chain
    \r\t8.  Seller confirms payment
    \r\t9.  Buyer confirms payment
    \r\t10. Pay for items in Cart
    \r\t11. Get Seller and Buyer Bitcoin Balances
    \r\t12. Process a Refund
    \r\t13. [Admin] Transfer Money (Between Seller/Buyer)
    \r------------------------------------------------\n
    """)
    
    choice = int(input("Please select an option from the above choices [1-13] or press 0 to exit: "))
    
    if choice == 0:
        print("\nExiting from Bitcoin Bridge System!")
        exit()
    elif choice == 1:
        print()
        deploy_system()
    elif choice == 2:
        print()
        connect_system()
    elif choice == 3:
        print()
        instructions()
    elif choice == 4:
        print()
        product_info()
    elif choice == 5:
        print()
        buy_items()
    elif choice == 6:
        print()
        change_item()
    elif choice == 7:
        print()
        add_more_item()
    elif choice == 8:
        print()
        seller_confirm()
    elif choice == 9:
        print()
        buyer_confirm()
    elif choice == 10:
        print()
        pay_for_item()
    elif choice == 11:
        print()
        bitcoin_wallet_info()
    elif choice == 12:
        print()
        process_refund()
    elif choice == 13:
        print()
        transfer_money()
    else:
        main()

def chip_choice():
    gate = int(input("Please enter the Gate Type of the product [1-2]: "))
    pins = int(input("Please enter the Pins Type of the product[1-4]: "))
    return gate, pins

def deploy_system():
    bcb.deploy_contracts()
    main()
    
def connect_system():
    bcb.connect()
    main()
    
def instructions():
    bcb.print_instructions()
    main()
    
def product_info():
    gate, pins = chip_choice()
    pinfo = bcb.get_product_info(gate, pins)
    print(f"""\nThe requested product has the following properties:
          \r\tName:\t\t{pinfo[0]}
          \r\tManufacturer:\t{pinfo[1]}
          \r\tDepartment:\t{pinfo[2]}
          \r\tPrice:\t\t${pinfo[3]/100}
          \r\tVoltage:\t{pinfo[4]/1000} V
          \r\tNum Left:\t{pinfo[5]}
          \r\tNum Gates:\t{pinfo[6]}""")
    main()
    
def buy_items():
    products = []
    for gate, pins in chips_tuple:
        products.append(int(input(f"Please enter the amount of {gate_dict[gate]}-{pins_dict[pins]}s you want to purchase: ")))
    
    print("Sending request to supply chain!")
    bcb.buy_items(products)
    print("Request sent!")
    main()
    
def change_item():
    gate, pins = chip_choice()
    price = int(input("Please enter the new price of the item in cents: "))
    voltage = int(input("Please enter the new voltage of the item in millivolts: "))
    print(f"Changing {gate_dict[gate]}-{pins_dict[pins]} info")
    bcb.change_item_info(gate, pins, price, voltage)
    main()

def add_more_item():
    gate, pins = chip_choice()
    num = int(input("Please enter the number of items you want to add: "))
    print(f"Adding {num} items to {gate_dict[gate]}-{pins_dict[pins]}")
    bcb.add_product(gate, pins, num)
    main()

def seller_confirm():
    receipt_num = int(input("Please enter the receipt number you received for your basket: "))
    print("Sending Confirmation from Seller")
    bcb.seller_confirmation(receipt_num, bcb.bridge_w3.eth.accounts[1])
    main()

def buyer_confirm():
    receipt_num = int(input("Please enter the receipt number you received for your basket: "))
    print("Sending Confirmation from Buyer")
    bcb.buyer_confirmation(receipt_num, bcb.bridge_w3.eth.accounts[2])
    print("Bitcoins have been reserved!")
    main()
    
def pay_for_item():
    receipt_num = int(input("Please enter the receipt number you received for your basket: "))
    print("Sending payment request")
    bcb.pay_basket(receipt_num)
    main()
    
def bitcoin_wallet_info():
    curr = input("Do you want to check balance in 'usd' or 'btc'? ")
    bcb.get_balance_btc(curr)
    main()
    
def process_refund():
    receipt_num = int(input("Please enter the receipt number you received for your basket: "))
    print("Sending refund request!")
    bcb.refund_basket(receipt_num)
    main()

def transfer_money():
    amount = int(input("Please enter the amount of money you want to transfer (US Cents): "))
    reverse = input("Do you want to send money from buyer to seller [y/n]? ")
    if reverse.lower() == 'y':
        reverse = False
    else:
        reverse = True
    bcb.send_btc(amount, reverse)
    main()
    
if __name__ == "__main__":
    main()