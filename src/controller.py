from screen import screenshot, reader
from input.listener import InputListener
import re


class Controller:
  def __init__(self, dictionary):
    self.input_listener = InputListener()
    self.hotkeys = []
    self.__register_hotkeys()

    self.dictionary = dictionary

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
    # TODO: Figure out how to make this customisable
    self.__register_hotkey(
        'request_partial_capture', '<ctrl>+<alt>+g', lambda: self.on_partial_capture())
    self.__register_hotkey(
        'request_full_capture', '<ctrl>+<alt>+h', lambda: self.on_full_capture())
    self.__register_hotkey(
        'exit', '<ctrl>+<alt>+e', lambda: self.on_exit_app())
    self.__register_hotkey(
        'show_monitor_info', '<ctrl>+<alt>+m', lambda: self.on_show_monitor_info())

    print("Registered {} hotkeys".format(len(self.hotkeys)))

  def on_full_capture(self):
    print('Capturing and processing all displays...')
    filenames = screenshot.take_full_screenshot()
    return self.__process_image(filenames)

  def on_partial_capture(self):
    print('Capturing and processing partial...')
    # TODO: Figure out how to make this customisable
    mon = screenshot.get_monitors()[2]
    monitor = {
        "top": mon["top"] + 100,
        "left": mon["left"] + 100,
        "width": 160,
        "height": 768,
        "mon": 2,
    }

    filenames = screenshot.take_partial_screenshot(monitor)
    return self.__process_image(filenames)

  def __process_image(self, filenames):
    print('Received {} files for processing, sending to OCR...'.format(len(filenames)))

    results = []
    for filename in filenames:
      print('Processing file: {}'.format(filename))
      result = reader.read_traditional(filename)
      results.extend(result)

    phrases = self.__parse_to_chinese_subphrases(results)
    print(phrases)

    print('Successfully processed files via OCR')
    return results

  def __remove_non_chinese_items(self, items):
    """Removes any items that do not contain Chinese from the results"""
    return list(filter(lambda x: re.match(r'[^A-Za-z\d\s]+', x), items))

  def __parse_to_chinese_subphrases(self, phrases):
    """
    Parses a list of phrases into smaller units.

    It first attempts to match as large of a word as possible, and adds that
    to the list of subphrases before continuing the search.

    The return value is a dictionary of the phrase to its subphrases.
    """
    phrases = self.__remove_non_chinese_items(phrases)

    phrases_map = {}

    for phrase in phrases:
      left, right, length = 0, 1, len(phrase)
      max_phrase_len = 0
      subphrases = []

      while left < length:
        curr = phrase[left:right]
        subphrase = self.dictionary.find_traditional(curr)

        if subphrase:
          max_phrase_len += 1

        if right >= length:
          # Add the longest phrase to subphrases
          subphrases.append(phrase[left:left+max_phrase_len])

          # Reset to start of next potential phrase
          if not max_phrase_len:
            left = left + 1
          else:
            left = left + max_phrase_len

          right = left
          max_phrase_len = 0

        # Move right pointer always
        right += 1

      subphrases = self.__remove_non_chinese_items(subphrases)
      phrases_map[phrase] = subphrases

    return phrases_map

  def on_show_monitor_info(self):
    print('Showing monitor info: {}'.format(screenshot.get_monitors()))

  def on_exit_app(self):
    print('Exiting application...')
    self.input_listener.stop()
