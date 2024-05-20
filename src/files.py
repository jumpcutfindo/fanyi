import os


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

    def is_directory_exists(self, directory):
        return os.path.isdir(directory)
