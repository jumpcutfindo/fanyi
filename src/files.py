import os
import json
from loguru import logger


class FileManager:
    def __init__(self):
        local_dir = self.get_local_directory()

        logger.info('Initializing file manager...')

        # Create a local app data folder if exists
        if not self.is_directory_exists(self.get_local_directory()):
            logger.info('Unable to find local directory for application')
            logger.info(
                f'Creating directories for local storage @ {local_dir}')
            os.makedirs(local_dir)

            # Create relevant subfolders
            os.makedirs(self.get_screenshots_directory())
        else:
            logger.info(f'Local storage found @ {local_dir}')

    def get_local_directory(self):
        return f'{os.getenv("LOCALAPPDATA")}\\fanyi'

    def get_screenshots_directory(self):
        return f'{self.get_local_directory()}\\screenshots'

    def get_presets_file(self):
        return f'{self.get_local_directory()}\\presets.json'

    def get_preferences_file(self):
        return f'{self.get_local_directory()}\\preferences.json'

    def load_presets_file(self):
        presets_file = self.get_presets_file()

        if (self.is_file_exists(presets_file)):
            logger.info('Presets file exists, loading...')
            f = open(presets_file, 'r', encoding='utf-8')
            return json.load(f)
        else:
            # Create empty file if not exists
            logger.info('Presets file not found, creating new...')
            f = open(presets_file, 'w', encoding='utf-8')

            # By default, we pass an empty dictionary of items
            json.dump({}, f, ensure_ascii=False, indent=4)
            f.close()
        return {}

    def save_presets_file(self, contents):
        logger.info(f'Saving {len(contents.keys())} presets...')
        presets_file = self.get_presets_file()

        def encoder(obj):
            return vars(obj)

        f = open(presets_file, 'w', encoding='utf-8')
        json.dump(contents, f, ensure_ascii=False, indent=4, default=encoder)
        f.close()

    def load_preferences_file(self):
        preferences_file = self.get_preferences_file()

        if (self.is_file_exists(preferences_file)):
            logger.info('Preferences file exists, loading...')
            f = open(preferences_file, 'r', encoding='utf-8')
            return json.load(f)
        else:
            # Create empty file if not exists
            logger.info('Preferences file not found, creating new...')
            f = open(preferences_file, 'w', encoding='utf-8')

            json.dump({}, f, ensure_ascii=False, indent=4)
            f.close()
        return {}

    def save_preferences_file(self, preferences):
        logger.info(f'Saving preferences...')
        presets_file = self.get_preferences_file()

        def encoder(obj):
            return vars(obj)

        f = open(presets_file, 'w', encoding='utf-8')
        json.dump(preferences, f, ensure_ascii=False,
                  indent=4, default=encoder)
        f.close()

    def is_file_exists(self, file):
        return os.path.exists(file)

    def is_directory_exists(self, directory):
        return os.path.isdir(directory)
