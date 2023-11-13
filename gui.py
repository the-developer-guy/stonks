from tkinter import ttk, PhotoImage
from coin import Wallet


class MainWindow:
    def __init__(self, root) -> None:
        self.root = root
        self.wallet = Wallet()

        self.mainframe = ttk.Frame(self.root)
        self.label = ttk.Label(self.mainframe, text="Your balance:")
        self.balance_label = ttk.Label(self.mainframe, text=self.wallet)

        self.placeholder_chart = PhotoImage(file="background.png")
        self.placeholder_chart_label = ttk.Label(self.mainframe, image=self.placeholder_chart)
        self._place()

    def _place(self):
        self.mainframe.grid()
        self.placeholder_chart_label.grid(row=0, column=0, rowspan=2)
        self.label.grid(row=0, column=1)
        self.balance_label.grid(row=1, column=1)
