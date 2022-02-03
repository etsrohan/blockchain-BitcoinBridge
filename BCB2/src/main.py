from functions.bcb_functions import BitcoinBridgeGanache

bcb = BitcoinBridgeGanache()

apparel_dict = {
    1: 'Shirt',
    2: 'T-Shirt',
    3: 'Pants'
}
fabric_dict = {
    1: 'Cotton',
    2: 'Polyester'
}
receipts = set()
clothes_tuple = (
    (1,1),
    (1,2),
    (2,1),
    (2,2),
    (3,1),
    (3,2)
)

def main():
    print("""\n------------------------------------------------
    \rWelcome to the Bitcoin Bridge System Demo!
    \rPlease select from one of the following options:
    \r\t1. Deploy System
    \r\t2. Connect to an already deployed system
    \r\t3. Instructions
    \r\t4. Get Product Information
    \r\t5. Add Products to Cart
    \r\t6. Change Item Information
    \r\t7. Add more Items in Supply Chain
    \r\t8. Seller confirms payment
    \r\t9. Buyer confirms payment
    \r\t10. Pay for items in Cart
    \r\t11. Get Seller and Buyer Bitcoin Balances
    \r------------------------------------------------\n
    """)
    
    choice = int(input("Please select an option from the above choices [1-11] or press 0 to exit: "))
    
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
    else:
        main()

def apparel_choice():
    apparel = int(input("Please enther the Apparel type of the product [1-3]: "))
    fabric = int(input("Please enter the Fabric of the product[1-2]: "))
    return apparel, fabric

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
    apparel, fabric = apparel_choice()
    pinfo = bcb.get_product_info(apparel, fabric)
    print(f"""\nThe requested product has the following properties:
          \r\tName:\t\t{pinfo[0]}
          \r\tManufacturer:\t{pinfo[1]}
          \r\tDepartment:\t{pinfo[2]}
          \r\tWeight:\t\t{pinfo[3]} grams
          \r\tPrice:\t\t${pinfo[4]/100}
          \r\tNum Left:\t{pinfo[5]}""")
    main()
    
def buy_items():
    products = []
    for apparel, fabric in clothes_tuple:
        products.append(int(input(f"Please enter the amount of {fabric_dict[fabric]} {apparel_dict[apparel]}s you want to purchase: ")))
    
    print("Sending request to supply chain!")
    bcb.buy_items(products)
    print("Request sent!")
    main()
    
def change_item():
    apparel, fabric = apparel_choice()
    price = int(input("Please enter the new price of the item in cents: "))
    weight = int(input("Please enter the new weight of the item in grams: "))
    print(f"Changing {fabric_dict[fabric]} {apparel_dict[apparel]} info")
    bcb.change_item_info(apparel, fabric, price, weight)
    main()

def add_more_item():
    apparel, fabric = apparel_choice()
    num = int(input("Please enter the number of items you want to add: "))
    print(f"Adding {num} items to {fabric_dict[fabric]} {apparel_dict[apparel]}")
    bcb.add_product(apparel, fabric, num)
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
    
if __name__ == "__main__":
    main()