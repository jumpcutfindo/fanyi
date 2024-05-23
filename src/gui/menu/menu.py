import tkinter as tk
from typing import TYPE_CHECKING

from .settings import SettingsFrameContainer
from .presets import PresetsFrameContainer

if TYPE_CHECKING:
    from gui.main import MainFrameContainer

class MenuFrameContainer:
    def __init__(self, parent: "MainFrameContainer"):
        self.parent = parent

        self.frame = tk.Frame(
            self.parent.frame, width=(self.parent.scale * 280))
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=8, pady=8)
        self.frame.pack_propagate(False)

        self.settings_frame = SettingsFrameContainer(self.parent, self)

        sep = tk.Frame(self.frame, height=2, bd=1, relief='sunken')
        sep.pack(side=tk.TOP, fill=tk.X, padx=8, pady=16)

        self.presets_frame = PresetsFrameContainer(self.parent, self)
