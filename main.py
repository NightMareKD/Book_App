import os
from tkinter import Tk
from gui import BookKeeperApp
from database import init_db

if not os.path.exists("exports"):
    os.makedirs("exports")

init_db()
root = Tk()
app = BookKeeperApp(root)
root.mainloop()
