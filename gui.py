from tkinter import ttk

class MainWindow:
    def __init__(self, root) -> None:
        self.root = root
        self.mainframe = ttk.Frame(self.root)
        self.label = ttk.Label(self.mainframe, text="Your balance:")
        self.balance_label = ttk.Label(self.mainframe, text="x")
        self._place()

    def _place(self):
        self.mainframe.grid()
        self.label.grid()
        self.balance_label.grid()
