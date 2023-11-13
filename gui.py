from tkinter import ttk, PhotoImage
from coin import Wallet


class MainWindow:
    def __init__(self, root: ttk.Frame) -> None:
        self.root = root
        self.mainframe = ttk.Frame(self.root)
        self.wallet = Wallet()

        self.balance = BalanceWidget(self.mainframe, self.wallet)
        self.balance.update_balance()

        self.trade = TradeWidget(self.mainframe, self.wallet)

        self.placeholder_chart = PhotoImage(file="background.png")
        self.placeholder_chart_label = ttk.Label(self.mainframe, image=self.placeholder_chart)
        
        self.trade.register_callback(self.balance.update_balance)
        self._configure_frames()
        self._grid()

    def _configure_frames(self):
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.columnconfigure(2, weight=1)

    def _grid(self):
        self.mainframe.grid(row=0, column=0, sticky="NWSE")
        self.placeholder_chart_label.grid(row=0, column=0, sticky="NWSE")
        self.balance.grid(row=0, column=1)
        self.trade.grid(row=0, column=2)

class BalanceWidget:
    def __init__(self, parent: ttk.Frame, wallet: Wallet) -> None:
        self.wallet = wallet
        self.frame = ttk.Frame(parent)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.label = ttk.Label(self.frame, text="Your balance:")
        self.balance_label = ttk.Label(self.frame, text="")

    def grid(self, row, column):
        self.frame.grid(row=row, column=column, sticky="NWSE")
        self.label.grid(row=0, column=0, sticky="NWSE")
        self.balance_label.grid(row=1, column=0, sticky="NWSE")

    def update_balance(self):
        self.balance_label["text"] = self.wallet

class TradeWidget:
    def __init__(self, parent: ttk.Frame, wallet: Wallet) -> None:
        self.wallet = wallet
        self.update_callback = None
        self.frame = ttk.Frame(parent)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.label = ttk.Label(self.frame, text="Exchange")
        self.coin = ttk.Entry(self.frame)
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
            coin = self.coin.get()
            self.wallet.buy(amount, coin)
        except Exception as e:
            print(e)
        if self.update_callback is not None:
            self.update_callback()

    def sell(self):
        try:
            amount = float(self.amount.get())
            coin = self.coin.get()
            self.wallet.sell(amount, coin)
        except Exception as e:
            print(e)
        if self.update_callback is not None:
            self.update_callback()
    
    def register_callback(self, f):
        self.update_callback = f
