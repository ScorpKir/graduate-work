"""Главное окно приложения"""

__author__ = 'Kirill Petryashev'

from enum import Enum
from typing import Tuple
import tkinter as tk

import numpy as np
import customtkinter as ctk

from gui.helper import validate_float_input, EquationParameters
from gui.portrait_window import PortraitWindow
from src.ode_storage import equation


class WindowParameters(Enum):
    """
    Параметры GUI основного окна
    """

    # Параметры окна
    TITLE: str = "TODO: Придумать название"
    LENGTH: int = 1400
    HEIGHT: int = 400

    # Параметры сетки
    ROWS_COUNT: int = 3
    COLUMNS_COUNT: int = 7
    WEIGHT: int = 1

    # Прочие декоративные параметры
    FONT = ('Colibri', 25)

class MainWindow(ctk.CTk):
    """Класс, реализующий интерфейс окна"""

    def __init__(self, fg_color: str | Tuple[str, str] | None = None,
                 **kwargs) -> None:
        # Создаём окно
        super().__init__(fg_color, **kwargs)

        # Конфигурируем окно
        self.__configure_window()

        # Конфигурируем сетку
        self.__configure_grid()

        # Конфигурируем переменные
        self.__configure_variables()

        # Задаем команду для валидации значений
        self.__validate_command = (self.register(validate_float_input), '%P')

        # Задаем виджеты
        self.__configure_widgets()

        # Запускаем приложение
        self.mainloop()

    def __configure_grid(self) -> None:
        """Конфигурация сетки"""

        self.rowconfigure(
            [
                row_number
                for row_number
                in range(WindowParameters.ROWS_COUNT.value)
            ],
            weight=WindowParameters.WEIGHT.value
        )
        self.columnconfigure(
            [
                column_number
                for column_number
                in range(WindowParameters.COLUMNS_COUNT.value)
            ],
            weight=WindowParameters.WEIGHT.value
        )

    def __configure_window(self) -> None:
        """Конфигурация окна"""

        self.title(WindowParameters.TITLE.value)
        self.geometry((
            f"{WindowParameters.LENGTH.value}x{WindowParameters.HEIGHT.value}"
        ))

    def __configure_variables(self) -> None:
        """Конфигурация переменных уравнения"""

        self.__x = tk.DoubleVar(
            self,
            value=EquationParameters.DEFAULT_X_VALUE.value)
        self.__x_prime = tk.DoubleVar(
            self,
            EquationParameters.DEFAULT_X_PRIME_VALUE.value
        )
        self.__mu = tk.DoubleVar(
            self,
            value=EquationParameters.DEFAULT_MU_VALUE.value
        )
        self.__a1 = tk.DoubleVar(
            self,
            value=EquationParameters.DEFAULT_A1_VALUE.value
        )
        self.__a2 = tk.DoubleVar(
            self,
            value=EquationParameters.DEFAULT_A1_VALUE.value
        )
        self.__a3 = tk.DoubleVar(
            self,
            value=EquationParameters.DEFAULT_A1_VALUE.value
        )

    def __configure_widgets(self) -> None:
        """Конфигурация виджетов"""

        # Поле ввода x(0)
        self.__x_label = ctk.CTkLabel(
            self,
            text='x(0): ',
            font=WindowParameters.FONT.value
        )
        self.__x_label.grid(row=0, column=0)
        self.__x_entry = ctk.CTkEntry(
            self,
            textvariable=self.__x,
            validate='key',
            validatecommand=self.__validate_command
        )
        self.__x_entry.grid(row=1, column=0)

        # Поле ввода x'(0)
        self.__x_prime_label = ctk.CTkLabel(
            self,
            text='x\'(0):',
            font=WindowParameters.FONT.value
        )
        self.__x_prime_label.grid(row=0, column=1)
        self.__x_prime_entry = ctk.CTkEntry(
            self,
            textvariable=self.__x_prime,
            validate='key',
            validatecommand=self.__validate_command
        )
        self.__x_prime_entry.grid(row=1, column=1)

        # Поле ввода mu
        self.__mu_label = ctk.CTkLabel(
            self,
            text='mu:',
            font=WindowParameters.FONT.value
        )
        self.__mu_label.grid(row=0, column=2)
        self.__mu_entry = ctk.CTkEntry(
            self,
            textvariable=self.__mu,
            validate='key',
            validatecommand=self.__validate_command
        )
        self.__mu_entry.grid(row=1, column=2)

        # Поле ввода a1
        self.__a1_label = ctk.CTkLabel(
            self,
            text='a1:',
            font=WindowParameters.FONT.value
        )
        self.__a1_label.grid(row=0, column=3)
        self.__a1_entry = ctk.CTkEntry(
            self,
            textvariable=self.__a1,
            validate='key',
            validatecommand=self.__validate_command
        )
        self.__a1_entry.grid(row=1, column=3)

        # Поле ввода a2
        self.__a2_label = ctk.CTkLabel(
            self,
            text='a2:',
            font=WindowParameters.FONT.value
        )
        self.__a2_label.grid(row=0, column=4)
        self.__a2_entry = ctk.CTkEntry(
            self,
            textvariable=self.__a2,
            validate='key',
            validatecommand=self.__validate_command
        )
        self.__a2_entry.grid(row=1, column=4)

        # Поле ввода a1
        self.__a3_label = ctk.CTkLabel(
            self,
            text='a3:',
            font=WindowParameters.FONT.value
        )
        self.__a3_label.grid(row=0, column=5)
        self.__a3_entry = ctk.CTkEntry(
            self,
            textvariable=self.__a3,
            validate='key',
            validatecommand=self.__validate_command
        )
        self.__a3_entry.grid(row=1, column=5)

        # Кнопка построения портрета
        self.__button = ctk.CTkButton(
            self,
            text='Построить',
            command=self.__on_build_button_click
        )
        self.__button.grid(row=1, column=6)

    def __on_build_button_click(self) -> None:
        """Обработчик кнопки 'построить'"""
        y0 = np.array([self.__x.get(), self.__x_prime.get()])
        t = np.linspace(0, 1, 100)
        mu = self.__mu.get()
        a1 = self.__a1.get()
        a2 = self.__a2.get()
        a3 = self.__a3.get()
        PortraitWindow(y0, equation, t, mu=mu, a1=a1, a2=a2, a3=a3)
