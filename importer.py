# Модуль импорта задач — загружаем задачи из внешних файлов
# Поддерживает CSV и JSON для миграции данных из других систем

import csv
import json
import os


class ImporterZadach:
    def __init__(self, filepath):
        self.filepath = filepath

    def _proverit_fayl(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Файл не найден: {self.filepath}")
        if os.path.getsize(self.filepath) == 0:
            raise ValueError("Файл пустой")

    def iz_csv(self):
        # импортируем задачи из CSV файла
        # ожидаемые колонки: название, приоритет, статус
        self._proverit_fayl()
        zadachi = []

        with open(self.filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for nomer, stroka in enumerate(reader, start=1):
                try:
                    zadachi.append({
                        "title": stroka["название"].strip(),
                        "priority": stroka.get("приоритет", "normal").strip(),
                        "done": stroka.get("статус", "").strip() == "выполнено"
                    })
                except KeyError as e:
                    print(f"! Строка {nomer}: отсутствует колонка {e}, пропускаем")

        print(f"✓ Импортировано задач из CSV: {len(zadachi)}")
        return zadachi

    def iz_json(self):
        # импортируем задачи из JSON файла
        self._proverit_fayl()

        with open(self.filepath, encoding="utf-8") as f:
            danye = json.load(f)

        if not isinstance(danye, list):
            raise ValueError("JSON должен содержать список задач")

        zadachi = []
        for nomer, item in enumerate(danye, start=1):
            try:
                zadachi.append({
                    "title": item["title"].strip(),
                    "priority": item.get("priority", "normal"),
                    "done": item.get("done", False)
                })
            except KeyError as e:
                print(f"! Запись {nomer}: отсутствует поле {e}, пропускаем")

        print(f"✓ Импортировано задач из JSON: {len(zadachi)}")
        return zadachi

    def opredelit_format(self):
        # определяем формат файла по расширению
        _, rasshirenie = os.path.splitext(self.filepath)
        if rasshirenie.lower() == ".csv":
            return self.iz_csv()
        elif rasshirenie.lower() == ".json":
            return self.iz_json()
        else:
            raise ValueError(f"Неподдерживаемый формат: {rasshirenie}")