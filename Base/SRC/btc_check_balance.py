from bit import PrivateKeyTestnet
import os

with open(os.path.join(os.getcwd(), "Wallet/wallet.info"), 'r') as file_obj:
    accs = file_obj.readlines()
accs[0] = accs[0][:-1]

keys = []
for acc in accs:
    keys.append(PrivateKeyTestnet(acc))

curr = input("Bitcoin ('btc') or USD ('usd'): ")
for key in keys:
    print(key.address)
    print(key.get_balance(curr))
    print()