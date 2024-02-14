import requests
import json
from datetime import datetime
import time
import os


class Coin:
    def __init__(self, name: str) -> None:
        self.name = name
        self.exchange_rate = []
        self.load_rate()
    
    def load_rate(self):
        if os.path.isfile(f"history/{self.name}.log"):
            with open(f"history/{self.name}.log", "rt", encoding="utf-8") as file:
                for line in file:
                    timestamp, value = line.split(",")
                    self.exchange_rate.append((timestamp, float(value)))
        if len(self.exchange_rate) == 0:
            self.exchange_rate.append((0,0))

    def update_rate(self, rate):
        if rate != self.exchange_rate[-1][1]:
            timestamp = int(time.time())
            self.exchange_rate.append((timestamp, rate))
            self.log_rate(timestamp, rate)
    
    def get_rate(self):
        try:
            rate = self.exchange_rate[-1][1]
        except Exception as e:
            rate = 0
        return rate

    def log_rate(self, timestamp: int, rate: float):
        with open(f"history/{self.name}.log", "at", encoding="utf-8") as file:
            file.write(f"{timestamp},{rate}\n")


class Exchange:
    
    def __init__(self, coins: set = set()) -> None:
        self.coins = {coin: Coin(coin) for coin in coins}
        self.current_exchange = {}
        self.exchange_history = []
        self.watched_coins = set()
        self.list_of_coins()
        if not os.path.isdir("history"):
            try:
                os.mkdir("history")
            except OSError as e:
                print("Couldn't make folder for coin history!")
                print(e)
                raise
        self.update()

    def list_of_coins(self):
        self.list = 'https://api.coingecko.com/api/v3/coins/list'
        try:
            self.response = requests.get(self.list)
            self.all_coins = json.loads(self.response.content.decode())
            self.supported_coins = [coin["id"] for coin in self.all_coins]
            print(f"{len(self.supported_coins)} coins supported!")
        except requests.exceptions.ConnectionError:
            print("Can't connect to the server!")
            self.supported_coins = []
            self.supported_coins.append("bitcoin")
            self.supported_coins.append("ethereum")
            self.supported_coins.append("dogecoin")
        except:
            print("We are probably rate limited!")
            self.supported_coins = []
            self.supported_coins.append("bitcoin")
            self.supported_coins.append("ethereum")
            self.supported_coins.append("dogecoin")
        self.coins_to_check = {coin for coin in self.coins if coin in self.supported_coins}

    def update(self):
        if len(self.coins_to_check) > 0:
            self.exhange_url = "https://api.coingecko.com/api/v3/simple/price?ids="
            for coin_name in self.coins_to_check:
                self.exhange_url += coin_name
                self.exhange_url += ","
            self.exhange_url += "&vs_currencies=usd"
            try:
                self.response = requests.get(self.exhange_url)
                decoded_response = json.loads(self.response.content.decode())
                if "status" in decoded_response:
                    status = decoded_response["status"]
                    print(f"Error! {status}")
                else:
                    self.current_exchange = decoded_response
                    for coin_name in self.coins:
                        current_coin = self.coins[coin_name]
                        current_rate = self._get_rate(coin_name)
                        current_coin.update_rate(current_rate)
            except Exception as e:
                print(e)
                print("Can't update exchange rates!")


    def _get_rate(self, coin):
        """For interal use only. Gets the current exhange rate."""
        rate = 0
        try:
            rate = self.current_exchange[coin]["usd"]
        except KeyError:
            print(f"Unknown coin: {coin}")
        return rate
    
    def get_rate(self, coin):
        """Gets the current exhange rate."""
        rate = 0
        try:
            rate = self.coins[coin].get_rate()
        except KeyError:
            print(f"Unknown coin: {coin}")
        return rate

    def add_coins(self, coins):
        match coins:
            case dict():
                for key in coins:
                    self.coins[key] = Coin(key)
            case str():
                self.coins.add({coins: Coin(coins)})
            case _:
                print("Unsupported input")
        self.coins_to_check = {coin for coin in self.coins if coin in self.supported_coins}
    
    def is_supported_coin(self, coin):
        return coin in self.supported_coins


class Wallet:
    def __init__(self, exchange: Exchange) -> None:
        self.coins = {}
        self.fiat = 0
        self.wallet_file_path = "wallet.json"
        self.load()
        self.exchange = exchange

    def __str__(self):
        summary = f"Wallet summary:\n{self.fiat:.2f} USD"
        self.exchange.update()
        for coin in self.coins:
            summary += f"\n{self.coins[coin]:.8g} {coin}"
        return summary

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
    
    def sum_amount(self):
        sum_usd = 0
        for coin in self.coins:
            if self.exchange.is_supported_coin(coin):
                sum_usd += self.exchange.get_rate(coin) * self.coins[coin]
        return sum_usd
    
    def total_in_usd(self):
        return self.sum_amount() + self.fiat

    def buy(self, amount: float, coin: str):
        if not self.exchange.is_supported_coin(coin):
            print(f"Unsupported coin: {coin}")
            raise TypeError(f"Unsupported coin: {coin}")
        if coin not in self.coins:
            self.coins[coin] = 0
        self.exchange.update()
        required_fiat = self.exchange.get_rate(coin) * amount
        if self.fiat >= required_fiat:
            self.fiat -= required_fiat
            self.coins[coin] += amount
            self.save()
            self.log_transaction(-required_fiat, coin, amount)
            return True
        else:
            return False

    def sell(self, amount: float, coin: str):
        if not self.exchange.is_supported_coin(coin):
            print(f"Unsupported coin: {coin}")
            raise TypeError(f"Unsupported coin: {coin}")
        available_amount = self.coins[coin]
        if coin not in self.coins:
            print(f"You don't have any of this coin: {coin}")
            return False
        if available_amount >= amount:
            self.exchange.update()
            fiat_got = amount * self.exchange.get_rate(coin)
            self.fiat += fiat_got
            self.coins[coin] -= amount
            self.save()
            self.log_transaction(fiat_got, coin, amount)
            return True
        else:
            return False
    
    def log_transaction(self, fiat_amount: float, coin: str, coin_amount: float):
        now = datetime.now()
        if fiat_amount < 0:
            log_message = f"Bought {coin_amount} {coin} for ${-fiat_amount:.2f} at {now};{fiat_amount};{coin_amount};{coin};{now}\n"
        else:
            log_message = f"Sold {coin_amount} {coin} for ${fiat_amount:.2f} at {now};{fiat_amount};{coin_amount};{coin};{now}\n"
        with open("ledger.log", "at", encoding="utf-8") as file:
            file.write(log_message)
