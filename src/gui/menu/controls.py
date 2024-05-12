import tkinter as tk

class ControlsFrame:
  def __init__(self, root, options_frame, controller):
    self.root = root
    self.options_frame = options_frame
    self.controller = controller

    self.controls_frame = tk.Frame(self.options_frame)
    self.controls_frame.pack(side=tk.TOP, fill=tk.X)

    self.__screenshot_control()

  def __screenshot_control(self):
    self.screenshot_control = tk.Button(self.controls_frame, text="Screenshot")
    self.screenshot_control.pack(side=tk.TOP, fill=tk.X)