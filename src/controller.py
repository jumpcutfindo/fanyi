import re
import pkuseg
from screen import screenshot, reader
from input.listener import InputListener


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
    mon = screenshot.get_monitors()[1]
    monitor = {
        "top": mon["top"] + 1080,
        "left": mon["left"] + 0,
        "width": 2560,
        "height": 180,
        "mon": 1,
    }

    filenames = screenshot.take_partial_screenshot(monitor)
    return self.__process_image(filenames)

  def __process_image(self, filenames):
    print('Received {} files for processing, sending to OCR...'.format(len(filenames)))

    results = []
    for filename in filenames:
      print('Processing file: {}'.format(filename))
      # TODO: Figure out how to make this customisable
      result = reader.read_simplified(filename)
      results.extend(result)

    phrases = self.__parse_to_chinese_subphrases(results)
    print(phrases)

    # TODO: Implement mapping to dictionary for definitions and pinyin

    print('Successfully processed files via OCR')
    return results

  def __remove_non_chinese_items(self, items):
    """Removes any items that do not contain Chinese from the results"""
    return list(filter(lambda x: re.match(r'[^A-Za-z\d\s]+', x), items))
  
  def __clean_words(self, items):
    """Removes items that are considered unclean, and removes symbols from words"""
    results = []
    for item in items:
      results.append(re.sub(r'[^\w\s]', '', item))
    
    results = list(filter(lambda x: re.match(r'\S', x), results))
    return results

  def __parse_to_chinese_subphrases(self, phrases):
    """
    Parses a list of phrases into smaller units.

    Uses `pkuseg` to help with the segmentation.
    """
    segmenter = pkuseg.pkuseg()
    phrases = self.__remove_non_chinese_items(phrases)

    phrases_map = {}

    for phrase in phrases:
      subphrases = segmenter.cut(phrase)
      subphrases = self.__remove_non_chinese_items(subphrases)
      phrases_map[phrase] = self.__clean_words(subphrases)

    return phrases_map

  def on_show_monitor_info(self):
    print('Showing monitor info: {}'.format(screenshot.get_monitors()))

  def on_exit_app(self):
    print('Exiting application...')
    self.input_listener.stop()
