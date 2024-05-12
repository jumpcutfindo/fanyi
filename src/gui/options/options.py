import tkinter as tk

from .settings import SettingsFrame
from .dimensions import DimensionsFrame
from .controls import ControlsFrame

class OptionsFrame:
  def __init__(self, root, controller):
    self.root = root
    self.controller = controller

    self.options_frame = tk.Frame(root, width=280)
    self.options_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=8, pady=8)
    self.options_frame.pack_propagate(0)

    self.settings_frame = SettingsFrame(root, self.options_frame, self.controller)

    sep = tk.Frame(self.options_frame, width=2, bd=1, relief='sunken')
    sep.pack(side=tk.TOP, fill=tk.X, padx=8, pady=8)

    self.dimensions_frame = DimensionsFrame(root, self.options_frame)

    self.controls_frame = ControlsFrame(root, self.options_frame, self.controller)