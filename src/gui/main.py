import tkinter as tk
from .options.options import OptionsFrame
from .result import ResultFrame

class MainFrame:
  def __init__(self):
    self.root = tk.Tk()
    self.root.title("Fanyi")
    self.root.geometry("800x600")

    self.main_frame = tk.Frame(self.root, bd=1, relief=tk.SOLID)
    self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    self.options_frame = OptionsFrame(self.main_frame)
    self.result_frame = ResultFrame(self.main_frame)

  def start(self):
    self.root.mainloop()
  