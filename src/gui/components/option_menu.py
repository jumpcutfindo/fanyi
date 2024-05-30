import tkinter as tk
from PIL import ImageTk, Image

class CustomOptionMenu(tk.OptionMenu):
    def __init__(self, master, variable, *options, command):

        tk.OptionMenu.__init__(self, master, variable, *options, command=command)

        self.config(indicatoron=False, width=12)

        image = Image.open('./assets/interface/caret-down.png').resize((20, 20))
        self.img = ImageTk.PhotoImage(image)
        self.img_label = tk.Label(self, image=self.img, height=12)
        self.img_label.place(relx=0.925, rely=0.5, anchor=tk.CENTER)
