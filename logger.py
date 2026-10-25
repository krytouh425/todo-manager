# Модуль логирования — записываем все действия пользователя
# Помогает отслеживать историю изменений задач

import os
from datetime import datetime

LOG_FILE = "todo.log"  # файл лога рядом со скриптом


class Logger:
    def __init__(self, filepath=LOG_FILE):
        self.filepath = filepath

    def _zapisat(self, uroven, soobshenie):
        # записываем строку в лог-файл
        vremya = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stroka = f"{vremya} [{uroven}] {soobshenie}\n"

        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(stroka)

    def info(self, soobshenie):
        self._zapisat("INFO", soobshenie)

    def warn(self, soobshenie):
        self._zapisat("WARN", soobshenie)

    def error(self, soobshenie):
        self._zapisat("ERROR", soobshenie)

    def deystvie(self, deystvie, detali=""):
        # логируем действие пользователя
        soobshenie = f"ACTION:{deystvie}"
        if detali:
            soobshenie += f" | {detali}"
        self._zapisat("INFO", soobshenie)

    def prochitat(self, poslednie=20):
        # читаем последние N строк лога
        if not os.path.exists(self.filepath):
            print("Лог-файл ещё не создан")
            return []

        with open(self.filepath, encoding="utf-8") as f:
            stroki = f.readlines()

        if not stroki:
            print("Лог-файл пустой")
            return []

        return [s.strip() for s in stroki[-poslednie:]]

    def filtr_po_urovnyu(self, uroven):
        # возвращаем только строки нужного уровня ERROR / WARN / INFO
        vse_stroki = self.prochitat(poslednie=1000)
        return [s for s in vse_stroki if f"[{uroven}]" in s]

    def statistika(self):
        # считаем количество записей по уровням
        vse = self.prochitat(poslednie=1000)
        return {
            "INFO": len([s for s in vse if "[INFO]" in s]),
            "WARN": len([s for s in vse if "[WARN]" in s]),
            "ERROR": len([s for s in vse if "[ERROR]" in s]),
            "vsego": len(vse)
        }

    def ochistit(self):
        # очищаем лог-файл
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
            print("✓ Лог очищен")
        else:
            print("Лог-файл не найден")