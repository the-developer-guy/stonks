import requests
import json
        

class Wallet:
    def __init__(self) -> None:
        self.coins = {}
        self.fiat = 0
        self.wallet_file_path = "wallet.json"
        self.list_of_coins()
        self.load()
        self.update()

    def __str__(self):
        summary = f"Wallet summary:\n{self.fiat:.2f} USD"
        self.update()
        for coin in self.coins:
            summary += f"\n{self.coins[coin]} {coin}"
        return summary
    
    def list_of_coins(self):
        self.list = 'https://api.coingecko.com/api/v3/coins/list'
        try:
            self.response = requests.get(self.list)
            self.all_coins = json.loads(self.response.content.decode())
            self.supported_coins = {coin["id"] for coin in self.all_coins}
        except requests.exceptions.ConnectionError:
            print("Can't connect to the server!")
            self.supported_coins = set()
            self.supported_coins.add("bitcoin")
            self.supported_coins.add("ethereum")
            self.supported_coins.add("dogecoin")
        except:
            print("We are probably rate limited!")
            self.supported_coins = set()
            self.supported_coins.add("bitcoin")
            self.supported_coins.add("ethereum")
            self.supported_coins.add("dogecoin")

    def load(self):
        try:
            with open(self.wallet_file_path, "rt", encoding="utf-8") as file:
                self.loaded_wallet = json.load(file)
                self.fiat = self.loaded_wallet["usd"]
                for coin in self.loaded_wallet["coins"]:
                    self.coins[coin["name"]] = coin["amount"]
        except:
            self.fiat = 10000
            self.coins = {}
    
    def save(self):
        try:
            coins_to_save = [{"name": coin,
                                        "amount": self.coins[coin]} 
                                        for coin in self.coins]
            wallet_to_save = {"usd": self.fiat, "coins": coins_to_save}
            with open(self.wallet_file_path, "wt", encoding="utf-8") as file:
                json.dump(wallet_to_save, file)
        except:
            print("Can't save the wallet data!")
    
    def update(self):
        self.exhange_url = "https://api.coingecko.com/api/v3/simple/price?ids="
        for coin_name in self.coins:
            self.exhange_url += coin_name
            self.exhange_url += ","
        self.exhange_url += "&vs_currencies=usd"
        try:
            self.response = requests.get(self.exhange_url)
            self.exchange = json.loads(self.response.content.decode())
        except:
            print("Can't update exchange rates!")
    
    def sum_amount(self):
        sum_usd = 0
        for coin in self.coins:
            if coin in self.supported_coins:
                sum_usd += self.exchange[coin]["usd"] * self.coins[coin]
        return sum_usd
    
    def get_exchange_rate(self, coin):
        rate = 0
        try:
            rate = self.exchange[coin]["usd"]
        except KeyError:
            print(f"Unknown coin: {coin}")
        return rate

    def buy(self, amount: float, coin: str):
        if coin not in self.supported_coins:
            print(f"Unsupported coin: {coin}")
            return False
        if coin not in self.coins:
            self.coins[coin] = 0
        self.update()
        required_fiat = self.get_exchange_rate(coin) * amount
        if self.fiat >= required_fiat:
            self.fiat -= required_fiat
            self.coins[coin] += amount
            self.save()
        return True

    def sell(self, amount: float, coin: str):
        available_amount = self.coins[coin]
        if coin not in self.coins:
            print(f"You don't have any of this coin: {coin}")
            return False
        if available_amount >= amount:
            self.update()
            self.fiat += amount * self.get_exchange_rate(coin)
            self.coins[coin] -= amount
            self.save()
            return True
