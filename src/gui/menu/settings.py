import tkinter as tk
from loguru import logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main import MainFrameContainer
    from gui.menu.menu import MenuFrameContainer

from tkinter.filedialog import askopenfilename


class SettingsFrameContainer:

    def __init__(self, root: "MainFrameContainer", parent: "MenuFrameContainer"):
        self.root = root
        self.parent = parent

        self.__load_supported_languages()

        self.frame = tk.Frame(self.parent.frame)
        self.frame.columnconfigure(1, weight=1)
        self.frame.pack(side=tk.TOP, fill=tk.X)

        settings_label = tk.Label(self.frame, text="Settings")
        settings_label.grid(row=0, column=0, sticky=tk.W, padx=0, pady=8)

        self.__dictionary_source_setting()
        self.__language_setting()

    def __dictionary_source_setting(self):
        dictionary_source_label = tk.Label(
            self.frame, text="Dictionary:")
        dictionary_source_label.grid(
            row=1, column=0, padx=(0, 16), pady=8, sticky=tk.W)

        # Dictionary file input
        self.dictionary_source_var = tk.StringVar(self.root.frame, "dict_src")
        self.dictionary_source_var.set(
            self.__get_saved_dictionary_path())  # Default selection
        dictionary_source_input = tk.Entry(
            self.frame, textvariable=self.dictionary_source_var)
        dictionary_source_input.config(state='disabled')
        dictionary_source_input.bind(
            "<1>", lambda event: dictionary_source_input.focus_set())
        dictionary_source_input.grid(row=1, column=1, sticky=tk.EW)

        # Dictionary label and select button
        bottom_right_frame = tk.Frame(self.frame)
        bottom_right_frame.grid(
            row=2, column=1, sticky=tk.NSEW, pady=8
        )

        dictionary_source_choose_file_btn = tk.Button(
            bottom_right_frame, text="Choose File", command=self.__choose_dict_file)
        dictionary_source_choose_file_btn.pack(side=tk.RIGHT)

        self.entry_count_var = tk.StringVar(self.root.frame, "entry_count")
        self.entry_count_label = tk.Label(
            bottom_right_frame, textvariable=self.entry_count_var
        )
        self.entry_count_label.pack(side=tk.RIGHT, padx=(0, 16))
        self.__set_displayed_entry_count(self.__get_entry_count())

    def __choose_dict_file(self):
        filename = askopenfilename()

        if not filename:
            logger.debug('User action: No file selected for dictionary')
            return

        logger.debug(f'User action: Selected dictionary "{filename}"')

        try:
            self.root.get_controller().parse_dictionary(filename)

            # Only update the value if successful
            self.dictionary_source_var.set(filename)
            self.__set_displayed_entry_count(self.__get_entry_count())
        except Exception as e:
            logger.error(f'Failed to parse dictionary: {e}')
            self.entry_count_var.set('Parse error')
            self.entry_count_label.config(fg='red')

    def __language_setting(self):
        language_label = tk.Label(self.frame, text="Language:")
        language_label.grid(row=3, column=0, padx=(0, 16), pady=8, sticky=tk.W)

        language_var = tk.StringVar(self.root.frame, "language")

        language_var.set(list(self.supported_languages.values())[0])
        language_dropdown = tk.OptionMenu(
            self.frame, language_var, *self.supported_languages.values(), command=self.__on_select_language)
        language_dropdown.grid(
            row=3, column=1, sticky=tk.NSEW
        )

    def __on_select_language(self, language):
        self.root.get_controller().set_language(language)
        logger.debug(f'User action: Selected language "{language}"')

    def __load_supported_languages(self):
        self.supported_languages = self.root.get_controller().get_supported_languages()

    def __get_saved_dictionary_path(self):
        path = self.root.get_preference_manager().load_preference('dictionaryPath')

        if not path:
            return '<No dictionary selected>'
        return path

    def __get_entry_count(self):
        dictionary = self.root.get_controller().get_dictionary()

        if not dictionary:
            return 0

        return dictionary.length()

    def __set_displayed_entry_count(self, count):
        if not self.entry_count_var or not self.entry_count_label:
            return

        self.entry_count_var.set(
            f'{self.__get_entry_count()} entries'
        )

        if count > 0:
            self.entry_count_label.config(fg='green')
        else:
            self.entry_count_label.config(fg='red')
