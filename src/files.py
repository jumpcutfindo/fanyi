import os
import json


class FileManager:
    def __init__(self):
        local_dir = self.get_local_directory()

        # Create a local app data folder if exists
        if not self.is_directory_exists(self.get_local_directory()):
            print(f'Creating directories for local storage @ {local_dir}')
            os.makedirs(local_dir)

            # Create relevant subfolders
            os.makedirs(self.get_screenshots_directory())
        else:
            print(f'Local storage found @ {local_dir}')

    def get_local_directory(self):
        return f'{os.getenv('LOCALAPPDATA')}\\fanyi'

    def get_screenshots_directory(self):
        return f'{self.get_local_directory()}\\screenshots'

    def get_presets_file(self):
        return f'{self.get_local_directory()}\\presets.json'

    def load_presets_file(self):
        presets_file = self.get_presets_file()

        if (self.is_file_exists(presets_file)):
            print('Presets file exists, loading...')
            return json.load(presets_file)
        else:
            # Create empty file if not exists
            print('Presets file not found, creating new...')
            f = open(presets_file, 'w', encoding='utf-8')
            json.dump({}, f, ensure_ascii=False, indent=4)
            f.close()
        return {}

    def save_presets_file(self, contents):
        presets_file = self.get_presets_file()

        f = open(presets_file, 'w', encoding='utf-8')
        json.dump(contents, f, ensure_ascii=False, indent=4)
        f.close()

    def is_file_exists(self, file):
        return os.path.exists(file)

    def is_directory_exists(self, directory):
        return os.path.isdir(directory)
