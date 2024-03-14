from tkinter import *
root = Tk()
canvas = Canvas(root, height=250, width=500)

canvas.create_line(25, 25, 350, 25, width=1)
canvas.create_line(25, 50, 350, 50, width=1)
canvas.create_line(25, 75, 350, 75, width=1)

boxradius = 10
canvas.create_rectangle(50-boxradius,25-boxradius,50+boxradius,25+boxradius, outline ="black", fill ="white", width = 1)
canvas.create_text(50, 25, fill ="black", text="H")




controlradius = 3
targetradius = 6
canvas.create_oval(100-controlradius,25-controlradius,100+controlradius,25+controlradius, outline = "white", fill = "white", width = 1)
canvas.create_oval(100-targetradius,50-targetradius,100+targetradius,50+targetradius, outline = "white", fill = "black", width = 1)
canvas.create_line(100, 25, 100, 50+targetradius, width=1)
canvas.create_line(100-targetradius, 50, 100+targetradius, 50, width=1)

canvas.pack()
root.mainloop()













# from tkinter import *
# import networkx as nx
# import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# root = Tk()

# f = Figure(figsize=(5,2))
# a = f.add_subplot(111)

# G = nx.Graph()
# G.add_edges_from([(1 ,2) , (2 ,3) , (1 ,3) , (1 ,4) ])
# nx.draw(G, ax=a)

# dagcanvas = FigureCanvasTkAgg(f, root)
# dagcanvas.get_tk_widget().pack()


# root.mainloop()