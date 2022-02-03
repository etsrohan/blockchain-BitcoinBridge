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
    ------------------------------------------------\n
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
        pass
    elif choice == 6:
        pass
    elif choice == 7:
        pass
    elif choice == 8:
        pass
    elif choice == 9:
        pass
    elif choice == 10:
        pass
    elif choice == 11:
        pass
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
    
if __name__ == "__main__":
    main()