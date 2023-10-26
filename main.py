from coin import Coin, Wallet


wallet = Wallet()

print(f"My current account's value is {wallet.sum_amount()} USD with {wallet.fiat} USD in fiat.")

menu_options = "\nCommands:\n\
    - update: get latest exchange rates and your portfolio\n\
    - buy amount coin: buy crypto, example: buy 0.1 bitcoin\n\
    - sell amount coin: buy crypto, example: sell 9001 dogecoin\n\
    - quit: save any changes left and quit\n"

while True:
    print(menu_options)
    user_input = input("What do you want? ")
    parts = user_input.split(" ")
    command = parts[0]
    if command == "update":
        pass
    elif command == "buy":
        pass
    elif command == "sell":
        pass
    elif command == "quit":
        wallet.save()
        break
    else:
        print("Unsupported command!")


