import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
from datetime import datetime
from coin import Wallet, Exchange


class MainWindow:
    def __init__(self, root: ttk.Frame) -> None:
        self.root = root
        self.mainframe = ttk.Frame(self.root)
        self.exchange = Exchange()
        self.wallet = Wallet(self.exchange)
        self.exchange.add_coins(self.wallet.coins)
        
        self.balance = BalanceWidget(self.mainframe, self.wallet)

        self.trade = TradeWidget(self.mainframe, self.wallet)
        self.chart = ChartWidget(self.mainframe)
        
        self.trade.register_callback(self.balance.update_balance)
        self._configure_frames()
        self._grid()
        self._update()

    def _update(self):
        self.exchange.update()
        self.balance.update_balance()
        self.root.after(30_000, self._update)

    def _configure_frames(self):
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.columnconfigure(2, weight=1)

    def _grid(self):
        self.mainframe.grid(row=0, column=0, sticky="NWSE")
        self.chart.grid(row=0, column=0)
        self.balance.grid(row=0, column=1)
        self.trade.grid(row=0, column=2)

class BalanceWidget:
    def __init__(self, parent: ttk.Frame, wallet: Wallet) -> None:
        self.wallet = wallet
        self.frame = ttk.Frame(parent)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=0)
        self.sum_label = ttk.Label(self.frame, 
                                   text="", 
                                   borderwidth=3, 
                                   relief="sunken", 
                                   justify=tk.LEFT, 
                                   anchor=tk.NW)
        self.balance_label = ttk.Label(self.frame, 
                                       text="", 
                                       borderwidth=3, 
                                       relief="sunken", 
                                       justify=tk.LEFT, 
                                       anchor=tk.NW)

    def grid(self, row, column):
        self.frame.grid(row=row, column=column, sticky="NWSE")
        self.sum_label.grid(row=0, column=0, sticky="NWSE")
        self.balance_label.grid(row=1, column=0, sticky="NWSE")

    def update_balance(self):
        now = datetime.now()
        self.sum_label["text"] = f"Total balance:\n{self.wallet.total_in_usd():.2f} USD\nLast updated: {now.strftime('%H:%M:%S')}"
        self.balance_label["text"] = self.wallet

class TradeWidget:
    def __init__(self, parent: ttk.Frame, wallet: Wallet) -> None:
        self.wallet = wallet
        self.update_callback = None
        self.frame = ttk.Frame(parent)
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=0)
        self.frame.rowconfigure(2, weight=0)
        self.frame.rowconfigure(3, weight=0)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.label = ttk.Label(self.frame, text="Exchange", borderwidth=3, relief="sunken")
        self.coin_var = tk.StringVar()
        self.coin = ttk.Combobox(self.frame, textvariable=self.coin_var, values=self.wallet.exchange.supported_coins)
        self.amount = ttk.Entry(self.frame)
        self.buy_button = ttk.Button(self.frame, text="Buy", command=self.buy)
        self.sell_button = ttk.Button(self.frame, text="Sell", command=self.sell)

    def grid(self, row, column):
        self.frame.grid(row=row, column=column, sticky="NWSE")
        self.label.grid(row=0, column=0, columnspan=2, sticky="NWSE")
        self.coin.grid(row=1, column=0, columnspan=2, sticky="NWSE")
        self.amount.grid(row=2, column=0, columnspan=2, sticky="NWSE")
        self.buy_button.grid(row=3, column=0, sticky="NWSE")
        self.sell_button.grid(row=3, column=1, sticky="NWSE")
    
    def buy(self):
        try:
            amount = float(self.amount.get())
            coin = self.coin_var.get()
            success = self.wallet.buy(amount, coin)
            if not success:
                messagebox.showwarning("Error", f"Transaction failed!\nNot enough USD in your wallet!")
        except TypeError as e:
            print(e)
            messagebox.showwarning("Error", "Invalid coin!")
        except ValueError as e:
            print(e)
            messagebox.showwarning("Error", "Invalid amount!")
        except Exception as e:
            print(e)
            messagebox.showwarning("Error", e)
        if self.update_callback is not None:
            self.update_callback()

    def sell(self):
        try:
            amount = float(self.amount.get())
            coin = self.coin_var.get()
            success = self.wallet.sell(amount, coin)
            if not success:
                messagebox.showwarning("Error", f"Transaction failed!\nNot enough {coin} in your wallet!")
        except ValueError as e:
            print(e)
            messagebox.showwarning("Error", "Invalid amount!")
        except TypeError as e:
            print(e)
            messagebox.showwarning("Error", "Invalid coin!")
        except Exception as e:
            print(e)
            messagebox.showwarning("Error", e)
        if self.update_callback is not None:
            self.update_callback()
    
    def register_callback(self, f):
        self.update_callback = f


class ChartWidget:
    def __init__(self, parent: ttk.Frame) -> None:
        self.frame = ttk.Frame(parent)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.placeholder_chart = PhotoImage(file="background.png")
        self.placeholder_chart_label = ttk.Label(self.frame, image=self.placeholder_chart, borderwidth=3, relief="sunken")

    def grid(self, row, column):
        self.frame.grid(row=row, column=column, sticky="NWSE")
        self.placeholder_chart_label.grid(row=0, column=0, sticky="NWSE")
