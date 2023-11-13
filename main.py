from tkinter import *
from tkinter import ttk
from coin import Wallet


wallet = Wallet()

print(wallet)
print(f"All your coins worth {wallet.sum_amount():.2f} USD plus {wallet.fiat} USD.")

root = Tk()
icon = PhotoImage(file="logo.png")
root.iconphoto(True, icon)
root.title("Stonks - trading simulator")

root.mainloop()
