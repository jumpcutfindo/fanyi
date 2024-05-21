import tkinter as tk


class TranslationsFrameContainer:
    def __init__(self, parent):
        self.parent = parent

        canvas = tk.Canvas(parent.frame)
        scrollbar = tk.Scrollbar(
            parent.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        canvas.create_window((0, 0), window=scrollable_frame,
                             anchor=tk.NW, tags=('canvas_frame'))
        canvas.bind('<Configure>', self.__handle_resize)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = canvas;
        self.frame = scrollable_frame

    def __handle_resize(self, event):
        canvas = event.widget
        canvas_frame = canvas.nametowidget(
            canvas.itemcget("canvas_frame", "window"))
        min_width = canvas_frame.winfo_reqwidth()
        min_height = canvas_frame.winfo_reqheight()
        if min_width < event.width:
            canvas.itemconfigure("canvas_frame", width=event.width)
        if min_height < event.height:
            canvas.itemconfigure("canvas_frame", height=event.height)

        canvas.configure(scrollregion=canvas.bbox("all"))

    def set_translations(self, translations):
        for index, (key, entries) in enumerate(translations.items()):
            containing_frame = tk.Frame(self.frame, background='white')
            containing_frame.pack(fill=tk.X, pady=8, padx=8, expand=True)

            # Sentence
            key_label = tk.Label(
                containing_frame, text=key, font=('Arial', 14), background='white')
            key_label.pack(padx=8, pady=8, anchor=tk.W)

            translation_frame = tk.Frame(containing_frame, background='white')
            translation_frame.pack(fill=tk.X, padx=8, pady=8, expand=True)
            translation_frame.columnconfigure(3, weight=1)

            if not entries or len(entries) == 0:
                not_exists_label = tk.Label(
                    translation_frame, text='No words found', font='Arial 10 italic', background='white')
                not_exists_label.grid(row=1, column=0, padx=8, pady=8, sticky=tk.W)
                continue
            
            # Insert each entry as a line
            for index, entry in enumerate(entries):
                if not entry:
                    continue

                simplified_label = tk.Label(translation_frame, text=f'{entry.simplified}', font=('Arial', 10), background='white')
                simplified_label.grid(row=index+1, column=0, padx=(0, 8), sticky=tk.NW)

                traditional_label = tk.Label(translation_frame, text=f'({entry.traditional})', font=('Arial', 10), background='white')
                traditional_label.grid(row=index+1, column=1, padx=8, sticky=tk.NW)

                pinyin_label = tk.Label(translation_frame, text=f'{entry.pinyin}', font=('Arial', 10), background='white')
                pinyin_label.grid(row=index+1, column=2, padx=8, sticky=tk.NW)

                definitions = []
                for i, d in enumerate(entry.definitions):
                    definitions.append(f'{i+1}. {d}')
                definitions_label = tk.Label(translation_frame, font=('Arial', 10), text='\n'.join(definitions), background='white', justify='left')                
                definitions_label.grid(row=index+1, column=3, padx=8, pady=(0, 24), sticky=tk.NW)
                