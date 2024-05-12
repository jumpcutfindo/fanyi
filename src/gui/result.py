import tkinter as tk

class ResultFrame:
  def __init__(self, root):
    self.root = root
    self.result_frame = tk.Frame(root, bd=1, relief=tk.SOLID)
    self.result_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    self.__screenshot_frame()
    self.__translation_frame()

  def __screenshot_frame(self):
    self.screenshot_frame = tk.Frame(self.result_frame, bd=1, relief=tk.SOLID)
    self.screenshot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
  
  def __translation_frame(self):
    self.translation_frame = tk.Frame(self.result_frame, bd=1, relief=tk.SOLID)
    self.translation_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
