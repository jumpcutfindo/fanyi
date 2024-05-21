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
        for key, words in translations.items():
            frame = tk.Frame(self.frame, bd=1, relief=tk.SOLID)
            frame.pack(fill=tk.X, pady=4, expand=True)

            key_label = tk.Label(frame, text=key, font=('Arial', 12, 'bold'))
            key_label.pack(anchor=tk.W, padx=5, pady=2)
