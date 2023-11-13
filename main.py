from tkinter import Tk, PhotoImage
from gui import MainWindow


root = Tk()
icon = PhotoImage(file="logo.png")
root.iconphoto(True, icon)
root.title("Stonks - trading simulator")

main_window = MainWindow(root)

root.mainloop()
