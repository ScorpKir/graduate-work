"""Окно отображения фазовой траектории"""

__author__ = 'Kirill Petryashev'

from typing import Tuple
from enum import Enum

import numpy as np
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from controllers.phase_controller import get_solution_by_initial_conditions


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


class WindowParameters(Enum):
    """
        Параметры GUI основного окна
    """

    # Параметры окна
    TITLE: str = "Траектория"

    # Прочие декоративные параметры
    FONT = ('Colibri', 25)


class PortraitWindow(ctk.CTk):
    """
        Окно, в котором производится отрисовка фазовой траектории
        дифференциального уравнения с заданными начальными условиями
    """

    def __init__(
        self,
        y0: np.ndarray,
        fg_color: str | Tuple[str, str] | None = None,
        **kwargs
    ):
        """
            :param: y0 Начальные условия для фазовой траектории
            :param kwargs: Остальные коэффициенты дифференциального уравнения
        """
        # Сегмент численного решения уравнения.
        # Вычисляется по хоту отображения графика.
        self.__sol = None

        # Инициализируем поля класса
        self.__init_params(y0, kwargs)

        # Вызываем конструктор базового класса
        super().__init__(fg_color, **kwargs)

        # Флаг, обозначающий отсутсвие паузы в рисовании.
        # Изменяется при нажатии ЛКМ пользователем
        self.__draw_mode = None

        # Конфигурируем окно
        self.__configure_window()

        # Отображаем фазовую траекторию на экране
        self.__configure_widgets()

        # Запускаем приложение
        self.mainloop()

    def __configure_window(self) -> None:
        """Конфигурация окна"""
        self.title(WindowParameters.TITLE.value)
        self.resizable(False, False)
        self.bind('<Button-1>', self.__on_left_mouse_click)
        self.bind('<Button-3>', self.__on_right_mouse_click)

    def __configure_widgets(self) -> None:
        """Конфигурация виджетов"""
        # Отображаем фазовую траекторию на графике
        self.__figure = Figure(figsize=(7, 7), dpi=100)
        self.__plot = self.__figure.add_subplot()
        self.__plot.plot(
            self.__sol[:, 0],
            self.__sol[:, 1],
            color='green',
            linewidth=3
        )

        # Создаем виджет и размещаем в окне
        self.canvas = FigureCanvasTkAgg(self.__figure, self)
        self.animation = FuncAnimation(
            self.__figure,
            self.__animate,
            interval=100
        )
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def __init_params(
        self,
        y0: np.ndarray,
        kwargs: dict['str', float]
    ) -> None:
        """
            Инициализация полей класса

            :param y0: Начальные значения x(0) и x'(0)a
            :param kwargs: Коэффициенты уравнения
        """
        coefficient_names = {'mu', 'a1', 'a2', 'a3'}
        self.__coefficients = {
            key: kwargs.pop(key, 0.0)
            for key in coefficient_names
        }
        self.__draw_mode = True
        self.__sol = get_solution_by_initial_conditions(
            y0,
            **self.__coefficients
        )

    def __animate(self, i):
        """Метод покадрового отображения анимации графика"""
        if self.__draw_mode:
            # Запоминаем последнюю точку
            y0 = self.__sol[-1]

            # Получаем продолжение траектории
            self.__sol = get_solution_by_initial_conditions(
                y0,
                **self.__coefficients
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

    # Параметр event используется во внутренних вызовах customtkinter
    # Поэтому для триггеров на нажатие кнопки отключим предупреждение
    # о неиспользуемых параметрах.

    # pylint: disable=unused-argument
    def __on_left_mouse_click(self, event):
        """Триггер на нажатие левой кнопки мыши"""
        self.__draw_mode = not self.__draw_mode

    def __on_right_mouse_click(self, event):
        """Триггер на нажатие правой кнопки мыши"""
        self.__plot.clear()
    # pylint: enable=unused-argument
