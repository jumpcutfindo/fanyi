import re
from typing import Callable, cast
import pkuseg
from loguru import logger

from dictionary import Dictionary, DictionaryEntry, Language, parse, segment_into_subphrases
from files import FileManager
from preferences import PreferenceManager
from presets import Preset
from screen import reader, screenshot
from input import InputListener


class Controller:
    def __init__(self, file_manager: FileManager, preference_manager: PreferenceManager):
        self.file_manager = file_manager
        self.preference_manager = preference_manager
        self.previous_preset = None

        self.input_listener = InputListener()
        self.hotkeys = []
        self.__register_hotkeys()

        self.dictionary: Dictionary | None = None
        self.language: Language = Language.SIMPLIFIED

        self.__try_load_dictionary()

    def start_input_listener(self):
        logger.info("Starting controller...")
        self.input_listener.start()

    def __register_hotkey(self, name: str, combo: str, action: Callable):
        self.hotkeys.append({
            name: name, combo: combo, action: action
        })
        self.input_listener.register_hotkey(name, combo, action)
        logger.debug(
            'Hotkey: Registered {} for action "{}"'.format(combo, name))

    def __register_hotkeys(self):
        logger.info("Registering hotkeys...")
        self.__register_hotkey(
            'capture_with_previous_preset', '<ctrl>+<alt>+g', lambda: self.on_capture_with_previous_preset())
        self.__register_hotkey(
            'show_monitor_info', '<ctrl>+<alt>+m', lambda: self.on_show_monitor_info())

        logger.info("Registered {} hotkeys".format(len(self.hotkeys)))

    def parse_dictionary(self, path: str):
        logger.info(f'Attempting to parse dictionary at "{path}"')

        if not self.file_manager.is_file_exists(path):
            logger.error(f'Specified dictionary file "{path}" does not exist!')

        try:
            self.dictionary = parse(path)

            # Save the path if parsing was successful
            self.preference_manager.save_preference('dictionaryPath', path)
        except Exception as e:
            logger.error(f'Unable to parse dictionary file "{path}": {e}')
            raise e

    def get_dictionary(self) -> Dictionary | None:
        return self.dictionary

    def __try_load_dictionary(self):
        logger.info('Checking if user previously loaded a dictionary...')
        saved_path = self.preference_manager.load_preference('dictionaryPath')

        if not saved_path:
            logger.info('No saved path for dictionary')
            return
        else:
            logger.info(
                'Saved path for dictionary found, attempting to parse...')
            self.parse_dictionary(saved_path)

    def set_language(self, language: Language | str):
        self.language = Language(language)

    def get_supported_languages(self) -> dict[str, str]:
        return {lang.name: lang.value for lang in Language}

    def on_partial_capture(self, preset: Preset):
        logger.info('Capturing and processing partial...')

        mon = screenshot.get_monitors()[preset.screen]
        settings = {
            "left": mon["left"] + preset.left,
            "top": mon["top"] + preset.top,
            "width": preset.width,
            "height": preset.height,
            "mon": preset.screen,
        }

        filename = screenshot.take_partial_screenshot(
            self.file_manager.get_screenshots_directory(), settings)
        return filename

    def process_image(self, filename: str):
        if not self.dictionary:
            raise ValueError('No dictionary loaded')

        if not filename:
            raise ValueError('No filenames provided')

        logger.info('Received {} files for processing, sending to OCR...'.format(
            len(filename)))

        read_text = []

        # Send file(s) for processing, adding to results
        logger.info('Processing file: {}'.format(filename))

        result = None

        # Process depending on the type of language the controller is set to
        if self.language == Language.TRADITIONAL:
            result = reader.read_traditional(filename)
        else:
            result = reader.read_simplified(filename)

        if result:
            logger.info(f'Successfully read {len(result)} lines!')
            read_text.extend(result)
        else:
            logger.warning(
                "OCR did not detect any text of the selected language in the image")

        # Break results into smaller segments
        logger.info('Segmenting lines into subphrases...')
        phrases = segment_into_subphrases(read_text)

        mapped_phrases = {}

        # Map the results to their dictionary entries
        logger.info('Mapping results to dictionary items...')
        for (phrase, subphrases) in phrases.items():
            xss = list(
                map(lambda p: self.__map_to_dictionary_entry(p), subphrases))
            mapped_phrases[phrase] = [x for xs in xss for x in xs]

        logger.success('Successfully processed files via OCR')
        return (filename, mapped_phrases)

    def __map_to_dictionary_entry(self, phrase: str) -> list[DictionaryEntry | None]:
        if not self.dictionary:
            return []

        result = []
        finder = self.dictionary.find_traditional if self.language == Language.TRADITIONAL else self.dictionary.find_simplified

        entry = finder(phrase)
        if not entry:
            # Unable to find the specified phrase in the dictionary
            # Break the phrase into smaller units and search
            result = list(map(lambda x: finder(x), phrase))
        else:
            result.append(entry)

        return result

    def set_previous_preset(self, preset: Preset):
        self.previous_preset = preset 

    def on_capture_with_previous_preset(self):
        if self.previous_preset == None:
            logger.error('Unable to capture with previous preset')
        else:
            self.on_partial_capture(self.previous_preset)

    def on_show_monitor_info(self):
        logger.info('Showing monitor info: {}'.format(
            screenshot.get_monitors()))

    def on_exit_app(self):
        logger.info('Exiting application...')
        self.input_listener.stop()

