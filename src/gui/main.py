import tkinter as tk

from .menu.menu import MenuFrame
from .result import ResultFrame

ORIGINAL_DPI = 95

class MainFrame:
  def __init__(self, controller, preset_manager):
    self.controller = controller
    self.preset_manager = preset_manager

    self.root = tk.Tk()
    self.root.title("Fanyi")

    # Scale according to current DPI
    scale = self.get_dpi() / ORIGINAL_DPI 
    self.root.geometry(f"{self.scaled(800, scale)}x{self.scaled(600, scale)}")

    self.main_frame = tk.Frame(self.root, bd=1, relief=tk.SOLID)
    self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    self.menu_frame = MenuFrame(self.main_frame, self.controller, self.preset_manager)
    self.result_frame = ResultFrame(self.main_frame, self.controller)

  def start(self):
    self.root.mainloop()

  def get_dpi(self):
    return self.root.winfo_fpixels('1i')
  
  def scaled(self, width, scale):
    return round(width * scale)