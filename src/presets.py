from files import FileManager


class Preset:
    def __init__(self, name: str, screen: int, left: int, top: int, width: int, height: int):
        self.name = name
        self.screen = screen
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    @staticmethod
    def from_json(json):
        return Preset(json['name'], json['screen'], json['left'], json['top'], json['width'], json['height'])


class PresetManager:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.__load_presets()

    def __load_presets(self):
        self.presets: list[Preset] = []
        self.preset_map: dict[str, Preset] = {}

        preset_map = self.file_manager.load_presets_file()
        for key in preset_map.keys():
            preset_json = preset_map[key]
            preset = Preset.from_json(preset_json)

            self.presets.append(preset)
            self.preset_map[key] = preset

    def create_preset(self, name: str, screen: int, left: int, top: int, width: int, height: int) -> Preset:
        return Preset(name, screen, left, top, width, height)

    def save_preset(self, name: str, screen: int, left: int, top: int, width: int, height: int):
        if name in self.preset_map.keys():
            # Preset exists, update existing
            preset = self.preset_map[name]
            preset.screen = screen
            preset.left = left
            preset.top = top
            preset.width = width
            preset.height = height
        else:
            preset = self.create_preset(name, screen, left, top, width, height)
            self.presets.append(preset)
            self.preset_map[name] = preset

        self.file_manager.save_presets_file(self.preset_map)

        return preset

    def get_preset(self, name: str):
        return self.preset_map[name]

    def list_presets(self):
        return self.presets

    def contains_preset(self, name: str):
        return name in self.preset_map

    def delete_preset(self, name: str):
        if not self.contains_preset(name):
            return

        self.presets.remove(self.get_preset(name))
        del self.preset_map[name]

        self.file_manager.save_presets_file(self.preset_map)
