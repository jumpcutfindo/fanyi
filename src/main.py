from ctypes import windll

import sys
from loguru import logger

from controller import Controller
from presets import PresetManager
from files import FileManager
from preferences import PreferenceManager

from gui.main import MainFrameContainer


def main():
    # Setup logger version
    logger.remove()
    logger.add(
        sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <lvl>{message}</lvl>", level="DEBUG")
    logger.info("Initializing application...")

    # Setup logical part of application
    file_manager = FileManager()
    preset_manager = PresetManager(file_manager)
    preference_manager = PreferenceManager()
    controller = Controller(file_manager, preference_manager)

    # Setup GUI stuff
    windll.shcore.SetProcessDpiAwareness(1)
    gui = MainFrameContainer(controller, preset_manager)
    gui.start()

    # TODO: Implement a way to manage this
    # dictionary = parser.parse(
    #     './.cache/cedict_ts.u8')

    # controller = Controller(dictionary)
    # controller.start()


if __name__ == "__main__":
    main()
