from bit import PrivateKeyTestnet
import os

my_key1 = PrivateKeyTestnet()
my_key2 = PrivateKeyTestnet()

print(my_key1.version)
print(my_key1.to_wif())
print(my_key1.address)
print()
print(my_key2.version)
print(my_key2.to_wif())
print(my_key2.address)

with open(os.path.join(os.getcwd(), "Wallet/wallet.info"), 'w') as file_obj:
    file_obj.write(my_key1.to_wif())
    file_obj.write('\n')
    file_obj.write(my_key2.to_wif())
    