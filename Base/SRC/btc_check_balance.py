from bit import PrivateKeyTestnet
import os

with open(os.path.join(os.getcwd(), "Wallet/wallet.info"), 'r') as file_obj:
    accs = file_obj.readlines()
accs[0] = accs[0][:-1]

keys = []
for acc in accs:
    keys.append(PrivateKeyTestnet(acc))

for key in keys:
    print(key.balance_as('usd'))
    print(key.address)