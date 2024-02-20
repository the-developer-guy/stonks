from tkinter import Tk, PhotoImage
from gui import MainWindow, resource_path


root = Tk()
icon = PhotoImage(file=resource_path("logo.png"))
root.iconphoto(True, icon)
root.title("Stonks - trading simulator")

main_window = MainWindow(root)

root.mainloop()
