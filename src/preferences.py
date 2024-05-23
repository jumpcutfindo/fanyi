from loguru import logger

from files import FileManager


class PreferenceManager:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager

        self.__load_all_preferences()

    def __load_all_preferences(self):
        self.preferences: dict[str, str] = self.file_manager.load_preferences_file()

    def save_preference(self, key: str, value: str):
        """
        Adds a preference to the internal dictionary and saves it to disk.

        Preferences should be in camel case.
        """
        self.preferences[key] = value

        self.file_manager.save_preferences_file(self.preferences)

    def load_preference(self, key: str):
        if not key in self.preferences:
            logger.warning(f'Unable to find preference: {key}')
            return None
        return self.preferences[key]
