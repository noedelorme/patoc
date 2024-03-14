from tkinter import * 
from gui.painter import CircuitPainter

class MainWindow:
    def __init__(self) -> None:
        root = Tk()
        root.title("Patoc: a graphical tool for quantum circuits")
        label = Label(root, text="Hello World")
        label.pack()

        canvas = Canvas(root, height=250, width=500)
        canvas.pack()
        config = {}
        painter = CircuitPainter(canvas, config)
        

        root.mainloop()

def printtest():
    print("This is a print from /app/window.py")