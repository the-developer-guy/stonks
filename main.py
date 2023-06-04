from coin import Coin, Wallet


wallet = Wallet()

print(f"My current account's value is {wallet.sum_amount()} USD with {wallet.fiat} USD in fiat.")

wallet.save()
