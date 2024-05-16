"""
Фрейм для работы с фазовыми траекториями.
"""

from typing import Final

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from views.frames.float_entry_frame import EntryFrame


class PhaseTrajectoryFrame(ctk.CTkFrame):
    """Фрейм работы с фазовыми траекториями"""

    # Обозначаем шрифт по умолчанию.
    FONT: Final = ('Colibri', 25)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Настраиваем сетку во фрейме.
        self.__configure_grid()

        # Настройка виджетов.
        self.__widgets_configure()

    def __configure_grid(self):
        """Настройка сетки"""
        self.grid_rowconfigure((0, 5), weight=0)
        self.grid_rowconfigure((1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((0, 7), weight=0)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6), weight=1)

    def __widgets_configure(self):
        """Настройка виджетов"""
        # Позиционируем виджет графика.
        self.__figure = Figure(figsize=(5, 4), dpi=100)
        self.__canvas = FigureCanvasTkAgg(figure=self.__figure, master=self)
        self.__canvas.get_tk_widget().grid(
            row=1,
            column=1,
            rowspan=4,
            columnspan=3,
            sticky='nsew'
        )

        # Позиционирую виджеты ввода значений
        self.__x_entry = EntryFrame('x(0)', value=0.0, master=self)
        self.__x_entry.grid(row=1, column=4, sticky='nsew', padx=10, pady=10)

        self.__x_derivative = EntryFrame("x'(0)", value=0.01, master=self)
        self.__x_derivative.grid(
            row=1,
            column=5,
            sticky='nsew',
            padx=10,
            pady=10
        )

        self.__mu = EntryFrame('mu', value=0.1, master=self)
        self.__mu.grid(row=2, column=4, sticky='nsew', padx=10, pady=10)

        self.__a1 = EntryFrame('a1', value=1.0, master=self)
        self.__a1.grid(row=3, column=4, sticky='nsew', padx=10, pady=10)

        self.__a2 = EntryFrame('a2', value=-1.0, master=self)
        self.__a2.grid(row=3, column=5, sticky='nsew', padx=10, pady=10)

        self.__a3 = EntryFrame('a3', value=1.0, master=self)
        self.__a3.grid(row=3, column=6, sticky='nsew', padx=10, pady=10)

        self.__draw_button = ctk.CTkButton(
            master=self,
            text='Старт',
            font=self.FONT
        )
        self.__draw_button.grid(
            row=4,
            column=4,
            sticky='nsew',
            padx=10,
            pady=10
        )

        self.__stop_button = ctk.CTkButton(
            master=self,
            text='Стоп',
            font=self.FONT
        )
        self.__stop_button.grid(
            row=4,
            column=5,
            sticky='nsew',
            padx=10,
            pady=10
        )

        self.__clear_button = ctk.CTkButton(
            master=self,
            text='Очистка',
            font=self.FONT
        )
        self.__clear_button.grid(
            row=4,
            column=6,
            sticky='nsew',
            padx=10,
            pady=10
        )
