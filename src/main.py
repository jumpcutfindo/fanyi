from ctypes import windll

import smokesignal
import sys
from loguru import logger

from controller import Controller
from presets import Preset, PresetManager
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
    global gui
    gui = MainFrameContainer(controller, preset_manager, preference_manager)

    gui.start()

@smokesignal.on('update_translation_results')
def update_translation_results(preset: Preset, result):
    if gui:
        gui.set_results(preset, result)    

if __name__ == "__main__":
    main()
