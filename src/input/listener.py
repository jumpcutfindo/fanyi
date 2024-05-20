from pynput import keyboard
from loguru import logger


class InputListener:
    def __init__(self):
        self.hotkeys = []

    def start(self):
        with keyboard.GlobalHotKeys(
                {x[1]: x[2] for x in self.hotkeys}) as h:
            self.listener = h
            h.join()

    def stop(self):
        keyboard.Listener.stop(self.listener)

    def register_hotkey(self, name: str, combo: str, action):
        def modified_action():
            logger.info('Combo {} pressed for action "{}"'.format(combo, name))
            action()

        self.hotkeys.append((name, combo, modified_action))
