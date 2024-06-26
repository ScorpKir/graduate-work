"""
Основной фрейм поиска циклов в фазовом поле
"""

from typing import Final
from tkinter import messagebox

import numpy as np
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from views.frames.float_entry_frame import EntryFrame
from controllers.phase_controller import (
    find_cycles_in_phase_field,
    get_solution_by_initial_conditions
)


class CycleFinderFrame(ctk.CTkFrame):
    """Фрейм работы с поиском циклов"""

    # Обозначаем шрифт по умолчанию.
    FONT: Final = ('Colibri', 25)

    # Обозначаем шаг для дополнительных траекторий
    HOP: Final = 0.004

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Настраиваем сетку во фрейме.
        self.__configure_grid()

        # Настройка виджетов
        self.__widgets_configure()

        # Настройка параметров уравнения
        self.__configure_equation()

    def __configure_grid(self):
        """Настройка сетки"""
        self.grid_rowconfigure((0, 7), weight=0)
        self.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.grid_columnconfigure((0, 7), weight=0)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6), weight=1)

    def __widgets_configure(self):
        """Настрока виджетов"""
        # Позиционирование графика
        self.__figure = Figure(dpi=100, facecolor='#2b2b2b')
        self.__plot = self.__figure.add_subplot()
        self.__plot.tick_params(axis='x', colors='white')
        self.__plot.tick_params(axis='y', colors='white')
        self.__plot.set_xlabel('x')
        self.__plot.set_ylabel("x'")
        self.__plot.xaxis.label.set_color('white')
        self.__plot.yaxis.label.set_color('white')
        self.__canvas = FigureCanvasTkAgg(figure=self.__figure, master=self)
        self.__canvas.get_tk_widget().grid(
            row=1,
            column=1,
            rowspan=6,
            columnspan=3,
            sticky='nsew'
        )
        self.__canvas.draw()

        # Позиционирование подсказывающих надписей
        self.__init_conditios_label = ctk.CTkLabel(
            self,
            text='Начальные условия',
            font=self.FONT
        )
        self.__init_conditios_label.grid(row=1, column=4, columnspan=3)

        # Позиционирование подсказывающих надписей
        self.__init_conditios_label = ctk.CTkLabel(
            self,
            text='Коэффициенты',
            font=self.FONT
        )
        self.__init_conditios_label.grid(row=3, column=4, columnspan=3)

        # Позиционирование виджетов ввода значений
        self.__x = EntryFrame('x(0)', value=0.0, master=self)
        self.__x.grid(row=2, column=4, sticky='nsew', padx=10, pady=10)

        self.__x_dot_min = EntryFrame("x'(0) min", value=0.01, master=self)
        self.__x_dot_min.grid(
            row=2,
            column=5,
            sticky='nsew',
            padx=10,
            pady=10
        )

        self.__x_dot_max = EntryFrame("x'(0) max", value=0.01, master=self)
        self.__x_dot_max.grid(
            row=2,
            column=6,
            sticky='nsew',
            padx=10,
            pady=10
        )

        self.__mu = EntryFrame('mu', value=0.1, master=self)
        self.__mu.grid(row=4, column=4, sticky='nsew', padx=10, pady=10)

        self.__a1 = EntryFrame('a1', value=1.0, master=self)
        self.__a1.grid(row=5, column=4, sticky='nsew', padx=10, pady=10)

        self.__a2 = EntryFrame('a2', value=-1.0, master=self)
        self.__a2.grid(row=5, column=5, sticky='nsew', padx=10, pady=10)

        self.__a3 = EntryFrame('a3', value=1.0, master=self)
        self.__a3.grid(row=5, column=6, sticky='nsew', padx=10, pady=10)

        self.__result_textbox = ctk.CTkTextbox(self)
        self.__result_textbox.grid(
            row=6,
            column=4,
            columnspan=2,
            sticky='nsew',
            padx=10,
            pady=10
        )

        self.__search_button = ctk.CTkButton(
            master=self,
            text='Поиск',
            font=self.FONT,
            command=self.__on_search_click
        )
        self.__search_button.grid(
            row=6,
            column=6,
            sticky='nsew',
            padx=10,
            pady=10
        )

    def __configure_equation(self) -> None:
        """Инициализируем все параметры, свазянные с уравнением"""
        # Коэффициенты уравнения, полученные из полей ввода
        self.__coefficients = {
            'mu': self.__mu.get(),
            'a1': self.__a1.get(),
            'a2': self.__a2.get(),
            'a3': self.__a3.get(),
        }

    # def __draw_arrow(self, sol: np.array, color: str = 'red') -> None:
    #     """Рисует стрелку направления для заданной траектории."""
    #     first_point = np.array([sol[len(sol) // 2, 0], sol[len(sol) // 2, 1]])
    #     second_point = np.array(
    #         [sol[len(sol) // 2 + 1, 0], sol[len(sol) // 2 + 1, 1]]
    #     )
    #     delta = second_point - first_point
    #     self.__plot.arrow(
    #         first_point[0],
    #         first_point[1],
    #         delta[0],
    #         delta[1],
    #         shape='full',
    #         lw=0,
    #         color=color,
    #         length_includes_head=True,
    #         head_width=delta[0]
    #     )

    def __on_search_click(self):
        """Триггер на нажатие кнопки поиска циклов"""
        if self.__x_dot_min.get() > self.__x_dot_max.get():
            messagebox.showerror(
                'Ошибка!',
                'Минимальное значение диопазона '
                'не может быть больше максимального!'
            )
            return

        self.__plot.clear()
        # Получаем траектории и начальные условия, где были обнаружены циклы
        self.__configure_equation()
        search_results = find_cycles_in_phase_field(
            self.__x.get(),
            self.__x_dot_min.get(),
            self.__x_dot_max.get(),
            **self.__coefficients
        )

        if len(search_results) != 0:
            self.__plot.plot(
                [self.__x.get(), self.__x.get()],
                [
                    self.__x_dot_min.get() - 20 * self.HOP, 
                    self.__x_dot_max.get() + 20 * self.HOP
                ],
                'k--'
            )
            text_fragments = [
                'Начальные условия, порождающие цикл: ',
                ''
            ]

            for result in search_results:
                start_point = result['start_point']
                text_fragments.append(f'({start_point[0]}, {start_point[1]})')
                sol = result['trajectory']
                self.__plot.plot(
                    sol[:, 0],
                    sol[:, 1],
                    color='green',
                    linewidth=1
                )
                # self.__draw_arrow(sol, 'black')

            another_points = [
                np.array(
                    [self.__x.get(), self.__x_dot_min.get() - 2 * self.HOP]
                ),
                np.array(
                    [self.__x.get(), self.__x_dot_min.get() - 4 * self.HOP]
                ),
                np.array(
                    [self.__x.get(), self.__x_dot_min.get() - 8 * self.HOP]
                ),
                np.array(
                    [self.__x.get(), self.__x_dot_max.get() + 2 * self.HOP]
                ),
                np.array(
                    [self.__x.get(), self.__x_dot_max.get() + 4 * self.HOP]
                ),
                np.array(
                    [self.__x.get(), self.__x_dot_max.get() + 8 * self.HOP]
                ),
            ]

            for point_ in another_points:
                self.__plot.plot(
                    point_[0],
                    point_[1],
                    'ko'
                )
                additional_sol = get_solution_by_initial_conditions(
                    point_,
                    **self.__coefficients
                )
                self.__plot.plot(
                    additional_sol[:, 0],
                    additional_sol[:, 1],
                    color='red',
                    linewidth=0.5
                )
                # self.__draw_arrow(additional_sol)

            self.__canvas.draw()

            points_to_show = '\n'.join(text_fragments)
            self.__result_textbox.delete(1.0, ctk.END)
            self.__result_textbox.insert(ctk.END, points_to_show)

        else:
            self.__result_textbox.delete(1.0, ctk.END)
            self.__result_textbox.insert(ctk.END, 'Циклы не найдены')
