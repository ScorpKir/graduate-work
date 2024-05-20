"""Главное окно приложения"""

__author__ = 'Kirill Petryashev'

from enum import Enum
from typing import Tuple

import customtkinter as ctk

from views.frames.phase_trajectory_frame import PhaseTrajectoryFrame
from views.frames.cycle_finder_frame import CycleFinderFrame


class WindowParameters(Enum):
    """
    Параметры GUI основного окна
    """

    # Параметры окна
    TITLE: str = "Дипломный проект"
    LENGTH: int = 1600
    HEIGHT: int = 900


class MainWindow(ctk.CTk):
    """Класс, реализующий интерфейс окна"""

    def __init__(self, fg_color: str | Tuple[str, str] | None = None,
                 **kwargs) -> None:
        # Создаём окно
        super().__init__(fg_color, **kwargs)

        # Конфигурируем окно
        self.__configure_window()

        # Задаем тему
        ctk.set_default_color_theme("green")

        # Задаем виджеты
        self.__configure_widgets()

        # Запускаем приложение
        self.mainloop()

    def __configure_window(self) -> None:
        """Конфигурация окна"""

        self.title(WindowParameters.TITLE.value)
        self.geometry((
            f"{WindowParameters.LENGTH.value}x{WindowParameters.HEIGHT.value}"
        ))

    def __configure_widgets(self) -> None:
        """Конфигурация виджетов"""
        # Создаём вкладки
        self.__tabview = ctk.CTkTabview(self)
        self.__first_tab = "Построение фазовой траектории"
        self.__tabview.add(self.__first_tab)
        self.__second_tab = "Поиск циклов в фазовом поле"
        self.__tabview.add(self.__second_tab)
        self.__tabview.set(self.__first_tab)
        self.__tabview.pack(fill='both', side='top', expand=True)

        self.__phase_frame = PhaseTrajectoryFrame(
            master=self.__tabview.tab(self.__first_tab)
        )
        self.__cycle_frame = CycleFinderFrame(
            master=self.__tabview.tab(self.__second_tab)
        )

        self.__phase_frame.pack(fill='both', side='top', expand=True)
        self.__cycle_frame.pack(fill='both', side='top', expand=True)
