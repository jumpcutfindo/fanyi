import tkinter as tk
from loguru import logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui import MainFrameContainer
    from gui.menu import MenuFrameContainer

from screen import screenshot


class PresetsFrameContainer:
    def __init__(self, root: "MainFrameContainer", parent: "MenuFrameContainer"):
        self.root = root
        self.parent = parent

        screen_info = self.__get_screen_info()
        self.screen_display_names = [
            f'{key}: {value["width"]}x{value["height"]}' for key, value in screen_info.items()]
        self.screen_display_to_info_map = {
            f'{key}: {value["width"]}x{value["height"]}': value for key, value in screen_info.items()}

        self.frame = tk.Frame(self.parent.frame)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(4, weight=1)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH,
                        padx=8, pady=(8, 0), expand=True)

        presets_label = tk.Label(self.frame, text="Presets")
        presets_label.grid(row=0, column=0, sticky=tk.W)

        self.__preset_config_section()
        self.__preset_list_section()
        self.__preset_controls_section()

    def __get_screen_info(self):
        screen_info = screenshot.get_monitors()

        screens = {}
        screens['Fullscreen'] = screen_info[0]
        screens['Fullscreen']['index'] = 0

        for i in range(1, len(screen_info)):
            name = 'Screen ' + str(i)
            screens[name] = screen_info[i]
            screens[name]['index'] = i

        return screens

    def __preset_config_section(self):
        # Preset configuration frame
        self.preset_config_frame = tk.Frame(self.frame)
        self.preset_config_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.preset_config_frame.grid_columnconfigure(1, weight=1)

        # Preset name configuration
        preset_name_label = tk.Label(self.preset_config_frame, text="Name:")
        preset_name_label.grid(
            row=0, column=0, sticky=tk.W, padx=(0, 16), pady=8)

        self.preset_name_var = tk.StringVar(self.root.frame)
        self.preset_name_var.set("New preset")
        preset_name_input = tk.Entry(
            self.preset_config_frame, textvariable=self.preset_name_var)
        preset_name_input.grid(row=0, column=1, sticky=tk.EW)

        # Screen configuration
        screen_value_label = tk.Label(self.preset_config_frame, text="Screen:")
        screen_value_label.grid(
            row=1, column=0, sticky=tk.W, padx=(0, 16), pady=8)

        self.screen_value_var = tk.StringVar(self.root.frame)
        screen_dropdown = tk.OptionMenu(self.preset_config_frame, self.screen_value_var,
                                        *self.screen_display_names, command=self.__on_screen_selected)
        screen_dropdown.grid(row=1, column=1, sticky=tk.NSEW, pady=8)

        # Dimensions configuration (top, left, height, width)
        self.dimension_values_frame = tk.Frame(self.frame)
        self.dimension_values_frame.columnconfigure([0, 1, 2, 3], weight=1)
        self.dimension_values_frame.grid(
            row=2, column=0, pady=8, sticky=tk.NSEW)

        # Dimensions - Left
        self.left_value_var = tk.IntVar(self.root.frame)
        self.left_value_var.set(0)

        left_value_frame = tk.Frame(self.dimension_values_frame)
        left_value_frame.grid(row=0, column=0, sticky=tk.NSEW)

        left_label = tk.Label(left_value_frame, text="L:")
        left_label.pack(side=tk.LEFT, padx=(0, 4))
        left_value_input = tk.Entry(
            left_value_frame, textvariable=self.left_value_var)
        left_value_input.pack(side=tk.LEFT, expand=True)

        # Dimensions - Top
        self.top_value_var = tk.IntVar(self.root.frame)
        self.top_value_var.set(0)

        top_value_frame = tk.Frame(self.dimension_values_frame)
        top_value_frame.grid(row=0, column=1, sticky=tk.NSEW)

        top_label = tk.Label(top_value_frame, text="T:")
        top_label.pack(side=tk.LEFT, padx=(0, 4))

        top_value_input = tk.Entry(
            top_value_frame, textvariable=self.top_value_var)
        top_value_input.pack(side=tk.LEFT, expand=True)

        # Dimensions - Width
        self.width_value_var = tk.IntVar(self.root.frame)
        self.width_value_var.set(0)

        width_frame = tk.Frame(self.dimension_values_frame)
        width_frame.grid(row=0, column=2, sticky=tk.NSEW)

        width_label = tk.Label(width_frame, text="W:")
        width_label.pack(side=tk.LEFT, padx=(0, 4))

        width_value_input = tk.Entry(
            width_frame, textvariable=self.width_value_var)
        width_value_input.pack(side=tk.LEFT, expand=True)

        # Dimensions - Height
        self.height_value_var = tk.IntVar(self.root.frame)
        self.height_value_var.set(0)

        height_frame = tk.Frame(self.dimension_values_frame)
        height_frame.grid(row=0, column=3, sticky=tk.NSEW)

        height_label = tk.Label(height_frame, text="H:")
        height_label.pack(side=tk.LEFT, padx=(0, 4))

        height_value_input = tk.Entry(
            height_frame, textvariable=self.height_value_var)
        height_value_input.pack(side=tk.LEFT, expand=True)

        # Preset controls
        self.preset_controls_frame = tk.Frame(self.frame)
        self.preset_controls_frame.grid(row=3, column=0, sticky=tk.EW, pady=8)
        self.preset_controls_frame.columnconfigure([0, 1, 2, 3], weight=1)

        delete_preset_button = tk.Button(
            self.preset_controls_frame, text="Delete", command=self.__on_delete_preset)
        delete_preset_button.grid(row=0, column=2, sticky=tk.EW, padx=8)

        save_preset_button = tk.Button(
            self.preset_controls_frame, text="Save", command=self.__on_save_preset)
        save_preset_button.grid(row=0, column=3, sticky=tk.EW)

        # Set default screen selection
        self.screen_value_var.set(self.screen_display_names[0])
        self.__on_screen_selected(self.screen_value_var.get())

    def __preset_list_section(self):
        self.preset_list_frame = tk.Frame(self.frame)
        self.preset_list_frame.grid(row=4, column=0, sticky=tk.NSEW, pady=8)

        self.preset_list_box = tk.Listbox(
            self.preset_list_frame, selectmode=tk.SINGLE)
        self.preset_list_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.preset_list_box.bind('<<ListboxSelect>>', self.__on_select_preset)

        self.__load_presets_into_listbox()

    def __preset_controls_section(self):
        self.preset_controls_frame = tk.Frame(self.frame)
        self.preset_controls_frame.grid(
            row=5, column=0, pady=8, sticky=tk.NSEW)
        self.preset_controls_frame.grid_columnconfigure(0, weight=1)

        screenshot_control = tk.Button(
            self.preset_controls_frame, text="Screenshot", command=self.__on_screenshot)
        screenshot_control.grid(row=0, column=0, sticky=tk.NSEW)

    def __on_screen_selected(self, screen_name):
        logger.debug(f'User action: Selected screen "{screen_name}"')

        screen_info = self.screen_display_to_info_map[screen_name]
        self.left_value_var.set(screen_info['left'])
        self.top_value_var.set(screen_info['top'])
        self.width_value_var.set(screen_info['width'])
        self.height_value_var.set(screen_info['height'])

    def __load_presets_into_listbox(self):
        """Clears the listbox and re-inserts all presets"""
        self.preset_list_box.delete(0, 'end')
        preset_list = self.__list_presets()

        for preset in preset_list:
            self.preset_list_box.insert('end', preset.name)

    def __on_select_preset(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        self.selected_preset = self.root.get_preset_manager().list_presets()[
            index]

        logger.debug(
            f'User action: Selected preset "{self.selected_preset.name}"')

        self.preset_name_var.set(self.selected_preset.name)
        self.screen_value_var.set(
            self.screen_display_names[self.selected_preset.screen])
        self.left_value_var.set(self.selected_preset.left)
        self.top_value_var.set(self.selected_preset.top)
        self.width_value_var.set(self.selected_preset.width)
        self.height_value_var.set(self.selected_preset.height)

    def __on_save_preset(self):
        preset_name = self.preset_name_var.get()
        screen = self.screen_display_to_info_map[self.screen_value_var.get(
        )]['index']
        left = self.left_value_var.get()
        top = self.top_value_var.get()
        width = self.width_value_var.get()
        height = self.height_value_var.get()

        logger.debug(f'User action: Saving preset {preset_name}')

        self.root.get_preset_manager().save_preset(
            preset_name, screen, left, top, width, height)

        self.__load_presets_into_listbox()

    def __on_delete_preset(self):
        preset_name = self.preset_name_var.get()
        self.root.get_preset_manager().delete_preset(preset_name)

        logger.debug(f'User action: Deleted preset {preset_name}')

        self.__load_presets_into_listbox()

    def __list_presets(self):
        return self.root.get_preset_manager().list_presets()

    def __get_preset_with_current_settings(self):
        """
        Returns a Preset with the current values populated in the input
        """
        return self.root.get_preset_manager().create_preset(
            name=self.preset_name_var.get(),
            screen=self.screen_display_to_info_map[self.screen_value_var.get(
            )]['index'],
            left=self.left_value_var.get(),
            top=self.top_value_var.get(),
            width=self.width_value_var.get(),
            height=self.height_value_var.get()
        )

    def __on_screenshot(self):
        current_preset = self.__get_preset_with_current_settings()
        self.root.on_screenshot(current_preset)
