import requests
import json

class Coin:
    def __init__(self, name, id, amount = 0) -> None:
        self.name = name
        self.id = id
        self.amount = amount
        

class Wallet:
    def __init__(self) -> None:
        self.coins = []
        self.fiat = 0
        self.wallet_file_path = "wallet.json"
        self.list_of_coins()
        self.load()
        self.update()
    
    def list_of_coins(self):
        self.list = 'https://api.coingecko.com/api/v3/coins/list'
        try:
            self.response = requests.get(self.list)
            print(self.response.content)
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
                    self.coins.append(Coin(coin["name"], coin["id"], coin["amount"]))
        except:
            self.fiat = 10000
            self.coins = []
    
    def save(self):
        try:
            with open(self.wallet_file_path, "wt", encoding="utf-8") as file:
                self.coins_to_save = [{"id": coin.id, "amount":coin.amount, "name": coin.name} for coin in self.coins]
                self.wallet_to_save = {"usd": self.fiat, "coins": self.coins_to_save}
                json.dump(self.wallet_to_save, file)
        except:
            print("Can't save the wallet data!")
    
    def update(self):
        self.exhange_url = "https://api.coingecko.com/api/v3/simple/price?ids="
        for coin in self.coins:
            self.exhange_url += coin.id
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
            if coin.id in self.supported_coins:
                sum_usd += self.exchange[coin.id]["usd"] * coin.amount
        return sum_usd

