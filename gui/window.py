from tkinter import * 

class MainWindow:
    def __init__(self) -> None:
        root = Tk()
        label = Label(root, text="Hello World")
        label.pack()
        root.mainloop()

def printtest():
    print("This is a print from /app/window.py")