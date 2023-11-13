from tkinter import ttk, PhotoImage
from coin import Wallet


class MainWindow:
    def __init__(self, root: ttk.Frame) -> None:
        self.root = root
        self.mainframe = ttk.Frame(self.root)
        self.wallet = Wallet()

        self.balance = BalanceWidget(self.mainframe)
        self.balance.set_balance(self.wallet)

        self.placeholder_chart = PhotoImage(file="background.png")
        self.placeholder_chart_label = ttk.Label(self.mainframe, image=self.placeholder_chart)
        
        self._configure_frames()
        self._grid()

    def _configure_frames(self):
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)

    def _grid(self):
        self.mainframe.grid(row=0, column=0, sticky="NWSE")
        self.placeholder_chart_label.grid(row=0, column=0, sticky="NWSE")
        self.balance.grid(row=0, column=1)

class BalanceWidget:
    def __init__(self, parent) -> None:
        self.frame = ttk.Frame(parent)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.label = ttk.Label(self.frame, text="Your balance:")
        self.balance_label = ttk.Label(self.frame, text="")

    def grid(self, row, column):
        self.frame.grid(row=row, column=column, sticky="NWSE")
        self.label.grid(row=0, column=0, sticky="NWSE")
        self.balance_label.grid(row=1, column=0, sticky="NWSE")

    def set_balance(self, balance):
        self.balance_label["text"] = balance
