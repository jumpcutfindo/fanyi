import tkinter as tk
from tkinter.filedialog import askopenfilename


class SettingsFrameContainer:

    def __init__(self, root, parent):
        self.root = root
        self.parent = parent

        self.frame = tk.Frame(self.parent.frame)
        self.frame.pack(side=tk.TOP, fill=tk.X)

        settings_label = tk.Label(self.frame, text="Settings")
        settings_label.pack(side=tk.TOP, pady=[0, 8], anchor=tk.NW)

        self.__dictionary_source_setting()
        self.__language_setting()

    def __dictionary_source_setting(self):
        self.dictionary_source_frame = tk.Frame(self.frame)
        self.dictionary_source_frame.pack(
            side=tk.TOP, fill=tk.BOTH, pady=[0, 8])

        dictionary_source_label = tk.Label(
            self.dictionary_source_frame, text="Dictionary")
        dictionary_source_label.pack(side=tk.TOP, anchor=tk.NW)

        # Dictionary file input
        dictionary_source_input_frame = tk.Frame(self.dictionary_source_frame)
        dictionary_source_input_frame.pack(side=tk.TOP, fill=tk.X)

        self.dictionary_source_var = tk.StringVar(self.root.frame, "dict_src")
        self.dictionary_source_var.set(
            "<no dictionary selected>")  # Default selection
        dictionary_source_input = tk.Entry(
            self.dictionary_source_frame, textvariable=self.dictionary_source_var)
        dictionary_source_input.pack(side=tk.LEFT, fill=tk.X, expand=True)

        dictionary_source_choose_file_btn = tk.Button(
            self.dictionary_source_frame, text="Choose File", command=self.__choose_dict_file)
        dictionary_source_choose_file_btn.pack(side=tk.LEFT)

    def __choose_dict_file(self):
        filename = askopenfilename()
        print(f'User selected dictionary: {filename}')

        try:
            self.root.get_controller().parse_dictionary(filename)

            # Only update the value if successful
            self.dictionary_source_var.set(filename)
        except:
            print(f'Failed to parse dictionary: {filename}')

    def __language_setting(self):
        self.language_frame = tk.Frame(self.frame)
        self.language_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=[0, 8])

        language_label = tk.Label(self.language_frame, text="Language:")
        language_label.pack(side=tk.LEFT)

        language_var = tk.StringVar(self.root.frame, "language")
        languages = self.root.get_controller().get_supported_languages()
        language_var.set(languages[0])  # Default selection
        language_dropdown = tk.OptionMenu(
            self.language_frame, language_var, *languages)
        language_dropdown.pack(side=tk.LEFT)
