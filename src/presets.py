class Preset:
    def __init__(self, name, screen, left, top, width, height):
        self.name = name
        self.screen = screen
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def from_json(json):
        return Preset(json['name'], json['screen'], json['left'], json['top'], json['width'], json['height'])


class PresetManager:
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.load_presets()

    def load_presets(self):
        self.presets = []
        self.preset_map = {}

        preset_map = self.file_manager.load_presets_file()
        for key in preset_map.keys():
            preset_json = preset_map[key]
            preset = Preset.from_json(preset_json)

            self.presets.append(preset)
            self.preset_map[key] = preset

    def create_preset(self, name, screen, left, top, width, height):
        return Preset(name, screen, left, top, width, height)

    def save_preset(self, name, screen, left, top, width, height):
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

    def get_preset(self, name):
        return self.preset_map[name]

    def list_presets(self):
        return self.presets

    def contains_preset(self, name):
        return name in self.preset_map

    def delete_preset(self, name):
        self.presets.remove(self.get_preset(name))
        del self.preset_map[name]
