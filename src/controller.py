from screen import screenshot, reader
from input.listener import InputListener
import re


class Controller:
  def __init__(self):
    self.input_listener = InputListener()
    self.hotkeys = []
    self.__register_hotkeys()

  def start(self):
    print("Starting controller...")
    self.input_listener.start()

  def __register_hotkey(self, name, combo, action):
    self.hotkeys.append({
        name: name, combo: combo, action: action
    })
    self.input_listener.register_hotkey(name, combo, action)
    print('Hotkey {} for action "{}"'.format(combo, name))

  def __register_hotkeys(self):
    print("Registering hotkeys...")
    self.__register_hotkey(
        'request_capture', '<ctrl>+<alt>+h', lambda: self.on_full_capture())
    self.__register_hotkey(
        'exit', '<ctrl>+<alt>+j', lambda: self.on_exit_app())
    print("Registered {} hotkeys".format(len(self.hotkeys)))

  def on_full_capture(self):
    print('Capturing and processing all displays...')
    filenames = screenshot.take_full_screenshot()

    print('Received {} files for processing, sending to OCR...'.format(len(filenames)))

    results = []
    for filename in filenames:
      print('Processing file: {}'.format(filename))
      result = reader.read_traditional(filename)
      print(result)
      results.append(
          list(filter(lambda x: re.findall(r'\\p{Han}', x), result)))

    print('Successfully processed files via OCR')
    print(results)
    return results

  def on_exit_app(self):
    print('Exiting application...')
    self.input_listener.stop()
