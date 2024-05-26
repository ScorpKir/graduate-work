"""
Окно с отображение прогресса поиска циклов.
"""

import customtkinter as ctk


class ProgressWindow(ctk.CTk):
    """Окно с отображением прогресса поиска циклов."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__progress_bar = ctk.CTkProgressBar(self)
        self.__progress_bar.pack(expand=True)

        self.mainloop()
