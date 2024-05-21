from loguru import logger


class PreferenceManager:
    def __init__(self, file_manager):
        self.file_manager = file_manager

        self.preferences = {}

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
