"""
Фрейм для работы с фазовыми траекториями.
"""

import tkinter as tk
from typing import Final

import numpy as np
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from views.frames.float_entry_frame import EntryFrame
from controllers.phase_controller import get_solution_by_initial_conditions


class PhaseTrajectoryFrame(ctk.CTkFrame):
    """Фрейм работы с фазовыми траекториями"""

    # Текущий фрагмент фазовой траектории
    __sol: np.array

    # Режим рисования (продолжение - True, пауза - False)
    __draw_mode: bool

    # Полная блокировка рисования без возможности продолжения
    __draw_lock: bool

    # Обозначаем шрифт по умолчанию.
    FONT: Final = ('Colibri', 25)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Настраиваем сетку во фрейме.
        self.__configure_grid()

        # Настройка виджетов.
        self.__widgets_configure()

        # Настройка уравнения и графика
        self.__configure_equation()

    def __configure_grid(self) -> None:
        """Настройка сетки"""
        self.grid_rowconfigure((0, 5), weight=0)
        self.grid_rowconfigure((1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((0, 7), weight=0)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6), weight=1)

    def __widgets_configure(self) -> None:
        """Настройка виджетов"""
        # Позиционируем виджет графика.
        self.__figure = Figure(figsize=(5, 4), dpi=100)
        self.__plot = self.__figure.add_subplot()
        self.__canvas = FigureCanvasTkAgg(figure=self.__figure, master=self)
        self.__canvas.get_tk_widget().grid(
            row=1,
            column=1,
            rowspan=4,
            columnspan=3,
            sticky='nsew'
        )
        self.__canvas.draw()

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
            font=self.FONT,
            command=self.__on_start_click
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
            font=self.FONT,
            command=self.__on_pause_click
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
            font=self.FONT,
            command=self.__on_clear_click
        )
        self.__clear_button.grid(
            row=4,
            column=6,
            sticky='nsew',
            padx=10,
            pady=10
        )

        # Настраиваем анимацию графика
        # pylint: disable=unused-private-member
        self.__animation = FuncAnimation(
            self.__figure,
            self.__animate,
            interval=100
        )
        # pylint: enable=unused-private-member

    def __configure_equation(self) -> None:
        """Инициализируем все параметры, свазянные с уравнением"""
        # Коэффициенты уравнения, полученные из полей ввода
        self.__coefficients = {
            'mu': self.__mu.get(),
            'a1': self.__a1.get(),
            'a2': self.__a2.get(),
            'a3': self.__a3.get(),
        }

        # Режим рисования (продолжение - True, пауза - False)
        self.__draw_mode = False
        # Полная блокировка рисования без возможности продолжения
        self.__draw_lock = False

        self.__sol = get_solution_by_initial_conditions(
            np.array([self.__x_entry.get(), self.__x_derivative.get()]),
            **self.__coefficients
        )

    def __animate(self, i):
        """Метод покадрового отображения анимации графика"""
        if self.__draw_mode and not self.__draw_lock:
            # Запоминаем последнюю точку
            y0 = self.__sol[-1]

            # Получаем продолжение траектории
            try:
                self.__sol = get_solution_by_initial_conditions(
                    y0,
                    **self.__coefficients
                )
            except ValueError:
                # pylint: disable=attribute-defined-outside-init
                self.__draw_lock = True
                # pylint: enable=attribute-defined-outside-init
                tk.messagebox.showinfo(
                    'Информация',
                    (
                        'Выход за пределы памяти в процессе вычисления.\n\n'
                        'Продолжение траектории невозможно.'
                    )
                )

            # Отображаем продолжение траектории
            self.__plot.plot(
                self.__sol[:, 0],
                self.__sol[:, 1],
                color='green',
                linewidth=3
            )

            if i % 10 == 0:
                # Определение координат и направления стрелки
                arrow_start = (self.__sol[0, 0], self.__sol[0, 1])
                arrow_end = (self.__sol[-1, 0], self.__sol[-1, 1])
                self.__plot.annotate(
                    "",
                    xytext=arrow_start,
                    xy=arrow_end,
                    arrowprops={
                        "arrowstyle": "->"
                    }
                )

    def __on_start_click(self):
        """Триггер на нажатие кнопки старта"""
        self.__draw_mode = True

    def __on_pause_click(self):
        """Триггер на нажатие кнопки паузы"""
        self.__draw_mode = False

    def __on_clear_click(self):
        """Триггер на нажатие кнопки очистки"""
        self.__plot.clear()
