"""
Фрейм для поля ввода
"""

from typing import Final
import tkinter as tk

import customtkinter as ctk


class EntryFrame(ctk.CTkFrame):
    """Фрейм для поля ввода"""

    # Обозначаем шрифт по умолчанию.
    FONT: Final = ('Colibri', 18)

    def __init__(self, value_name: str, value: float = 0.0, **kwargs):
        """
        Конструктор класса

        :param value_name: Название величины для ввода.
        :param value: Значение величины по умолчанию.
        :param kwargs: Остальные параметры фрейма.
        """
        # Конструктор базового класса.
        super().__init__(**kwargs)

        # Фиксируем название величины.
        self.__value_name = value_name

        # Создаём переменную, куда будем класть значения
        self.__variable = tk.DoubleVar(
            self,
            value=value
        )

        # Задаем команду для валидации значений
        self.__validate_command = (
            self.register(self.__validate_float_input),
            '%P'
        )

        # Создаём заголовок с названием величины.
        self.__label = ctk.CTkLabel(
            self,
            text=self.__value_name,
            font=self.FONT
        )
        self.__label.pack(expand=True)

        # Создаём само поле ввода.
        self.__entry = ctk.CTkEntry(
            self,
            textvariable=self.__variable,
            validate='key',
            validatecommand=self.__validate_command
        )
        self.__entry.pack(expand=True)

    def __validate_float_input(self, value: str) -> bool:
        """
        Метод проверяет возможность конвертирования
        строки в число с плавающей точкой.

        :param value: Текстовое значение для валидации.
        :return: Логическое значение, обозначающее валидность строки.
        """
        if value not in (None, '', '-'):
            try:
                float(value)
            except ValueError:
                return False
        return True

    def get(self) -> float:
        """Получить значение из поля ввода."""
        return self.__variable.get()
