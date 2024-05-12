import tkinter as tk

from .settings import SettingsFrame
from .presets import PresetsFrame
from .controls import ControlsFrame

class MenuFrame:
  def __init__(self, root, controller):
    self.root = root
    self.controller = controller

    self.menu_frame = tk.Frame(root, width=280)
    self.menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=8, pady=8)
    self.menu_frame.pack_propagate(0)

    self.settings_frame = SettingsFrame(root, self.menu_frame, self.controller)

    sep = tk.Frame(self.menu_frame, width=2, bd=1, relief='sunken')
    sep.pack(side=tk.TOP, fill=tk.X, padx=8, pady=8)

    self.dimensions_frame = PresetsFrame(root, self.menu_frame)

    self.controls_frame = ControlsFrame(root, self.menu_frame, self.controller)