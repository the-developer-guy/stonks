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
        self.list_of_coins()
        self.load_wallet()
        self.update()
    
    def list_of_coins(self):
        self.list = 'https://api.coingecko.com/api/v3/coins/list'
        self.response = requests.get(self.list)
        self.all_coins = json.loads(self.response.content.decode())
        self.supported_coins = {coin["id"] for coin in self.all_coins}
    
    def load_wallet(self):
        self.coins.append(Coin("Bitcoin", "bitcoin", 1))
        self.coins.append(Coin("Ethereum", "ethereum", 5))
        self.coins.append(Coin("Dogecoin", "dogecoin", 9001))
        self.coins.append(Coin("Not existing coin", "noexistcoin", 9001))
    
    def update(self):
        self.exhange_url = "https://api.coingecko.com/api/v3/simple/price?ids="
        for coin in self.coins:
            self.exhange_url += coin.id
            self.exhange_url += ","
        self.exhange_url += "&vs_currencies=usd"
        self.response = requests.get(self.exhange_url)
        self.exchange = json.loads(self.response.content.decode())
    
    def sum_amount(self):
        sum_usd = 0
        for coin in self.coins:
            if coin.id in self.supported_coins:
                sum_usd += self.exchange[coin.id]["usd"] * coin.amount
        return sum_usd

