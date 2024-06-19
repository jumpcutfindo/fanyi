import tkinter as tk
from typing import TYPE_CHECKING

from .settings import SettingsFrameContainer
from .presets import PresetsFrameContainer

if TYPE_CHECKING:
    from gui import MainFrameContainer


class MenuFrameContainer:
    def __init__(self, parent: "MainFrameContainer"):
        self.parent = parent

        self.frame = tk.Frame(
            self.parent.frame, width=(self.parent.scale * 280))
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.frame.pack_propagate(False)

        self.settings_frame = SettingsFrameContainer(self.parent, self)

        sep = tk.Frame(self.frame, height=2, bd=1, relief='sunken')
        sep.pack(side=tk.TOP, fill=tk.X)

        self.presets_frame = PresetsFrameContainer(self.parent, self)
    
    def enable_processing(self):
        self.presets_frame.enable_processing()
    
    def disable_processing(self):
        self.presets_frame.disable_processing()