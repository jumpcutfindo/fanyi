import re
from typing import Callable, cast
import pkuseg
from loguru import logger

from dictionary import Dictionary, DictionaryEntry, Language, parse
from files import FileManager
from preferences import PreferenceManager
from presets import Preset
from screen import reader, screenshot
from input import InputListener


class Controller:
    def __init__(self, file_manager: FileManager, preference_manager: PreferenceManager):
        self.file_manager = file_manager
        self.preference_manager = preference_manager

        self.input_listener = InputListener()
        self.hotkeys = []
        self.__register_hotkeys()

        self.dictionary: Dictionary | None = None
        self.language: Language = Language.SIMPLIFIED

        self.__try_load_dictionary()

    def start(self):
        logger.info("Starting controller...")
        self.input_listener.start()

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

    def __register_hotkey(self, name: str, combo: str, action: Callable):
        self.hotkeys.append({
            name: name, combo: combo, action: action
        })
        self.input_listener.register_hotkey(name, combo, action)
        logger.debug(
            'Hotkey: Registered {} for action "{}"'.format(combo, name))

    def __register_hotkeys(self):
        logger.info("Registering hotkeys...")
        # TODO: Figure out how to make this customisable
        self.__register_hotkey(
            'exit', '<ctrl>+<alt>+e', lambda: self.on_exit_app())
        self.__register_hotkey(
            'show_monitor_info', '<ctrl>+<alt>+m', lambda: self.on_show_monitor_info())

        logger.info("Registered {} hotkeys".format(len(self.hotkeys)))

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

        filenames = screenshot.take_partial_screenshot(
            self.file_manager.get_screenshots_directory(), settings)
        return self.process_image(filenames)

    def process_image(self, filenames: list[str]):
        if not self.dictionary:
            raise ValueError('No dictionary loaded')

        if not filenames:
            raise ValueError('No filenames provided')

        logger.info('Received {} files for processing, sending to OCR...'.format(
            len(filenames)))

        read_text = []

        # Send file(s) for processing, adding to results
        for filename in filenames:
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
        logger.info('Breaking lines into subphrases...')
        phrases = self.__parse_to_chinese_subphrases(read_text)

        mapped_phrases = {}

        # Map the results to their dictionary entries
        logger.info('Mapping results to dictionary items...')
        for (phrase, subphrases) in phrases.items():
            xss = list(
                map(lambda p: self.__map_to_dictionary_entry(p), subphrases))
            mapped_phrases[phrase] = [x for xs in xss for x in xs]

        logger.success('Successfully processed files via OCR')
        return (filenames, mapped_phrases)

    def __remove_non_chinese_items(self, items: list[str]) -> list[str]:
        """Removes any items that do not contain Chinese from the results"""
        return list(filter(lambda x: re.match(r'[^A-Za-z\d\s]+', x), items))

    def __clean_words(self, items: list[str]) -> list[str]:
        """Removes items that are considered unclean, and removes symbols from words"""
        results = []
        for item in items:
            results.append(re.sub(r'[^\w\s]', '', item))

        results = list(filter(lambda x: re.match(r'\S', x), results))
        return results

    def __parse_to_chinese_subphrases(self, phrases) -> dict[str, list[str]]:
        """
        Parses a list of phrases into smaller units.

        Uses `pkuseg` to help with the segmentation.
        """
        segmenter = pkuseg.pkuseg()
        phrases = self.__remove_non_chinese_items(phrases)

        phrases_map = {}

        for phrase in phrases:
            subphrases = cast(list[str], segmenter.cut(phrase))
            subphrases = self.__remove_non_chinese_items(subphrases)
            phrases_map[phrase] = self.__clean_words(subphrases)

        return phrases_map

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

    def on_show_monitor_info(self):
        logger.info('Showing monitor info: {}'.format(
            screenshot.get_monitors()))

    def on_exit_app(self):
        logger.info('Exiting application...')
        self.input_listener.stop()
