from ctypes import windll

import sys
from loguru import logger

from controller import Controller
from presets import PresetManager
from files import FileManager
from preferences import PreferenceManager

from gui import MainFrameContainer


def main():
    # Setup logger version
    logger.remove()
    logger.add(
        sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <lvl>{message}</lvl>", level="DEBUG")
    logger.info("Initializing application...")

    # Setup logical part of application
    file_manager = FileManager()
    preset_manager = PresetManager(file_manager)
    preference_manager = PreferenceManager(file_manager)
    controller = Controller(file_manager, preference_manager)

    # Start key listeners
    controller.start_input_listener()

    # Setup GUI stuff
    windll.shcore.SetProcessDpiAwareness(1)
    gui = MainFrameContainer(controller, preset_manager, preference_manager)

    gui.start()

    # Setup on close stuff
    gui_root = gui.get_root()
    gui_root.protocol("WM_DELETE_WINDOW", lambda: on_close(gui, controller))

def on_close(gui: MainFrameContainer, controller: Controller):
    controller.on_exit_app()

if __name__ == "__main__":
    main()
