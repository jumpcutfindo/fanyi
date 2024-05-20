class Preset:
    def __init__(self, name, screen, left, top, width, height):
        self.name = name
        self.screen = screen
        self.left = left
        self.top = top
        self.width = width
        self.height = height


class PresetManager:
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.load_presets()

    def load_presets(self):
        self.preset_map = self.file_manager.load_presets_file()
        self.presets = []

        for key in self.preset_map.keys():
            self.presets.append(self.preset_map[key])

    def create_preset(self, name, screen, left, top, width, height):
        return Preset(name, screen, left, top, width, height)

    def add_preset(self, name, screen, left, top, width, height):
        preset = self.create_preset(name, screen, left, top, width, height)
        self.presets.append(preset)
        self.preset_map[name] = preset

        return preset

    def get_preset(self, name):
        return self.preset_map[name]

    def list_presets(self):
        return self.presets

    def delete_preset(self, name):
        self.presets.remove(self.get_preset(name))
        del self.preset_map[name]
