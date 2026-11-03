# Модуль архивации — переносим старые задачи в архив
# Используется для разгрузки основного списка задач команды

import json
import os
from datetime import datetime

ARCHIVE_FILE = "tasks_archive.json"  # файл архива


class ArkhivZadach:
    def __init__(self, filepath=ARCHIVE_FILE):
        self.filepath = filepath

    def _zagruzit(self):
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, encoding="utf-8") as f:
            return json.load(f)

    def _sohranit(self, danye):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(danye, f, ensure_ascii=False, indent=2)

    def arhivirovat(self, tasks):
        # переносим задачи в архив
        arhiv = self._zagruzit()
        vremya = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for t in tasks:
            zapis = t.to_dict()
            zapis["arhivirovano"] = vremya
            arhiv.append(zapis)

        self._sohranit(arhiv)
        print(f"✓ Архивировано задач: {len(tasks)}")

    def poisk_v_arhive(self, zapros):
        # ищем задачи в архиве по ключевому слову
        arhiv = self._zagruzit()
        zapros = zapros.lower()
        return [z for z in arhiv if zapros in z["title"].lower()]

    def statistika_arhiva(self):
        arhiv = self._zagruzit()
        if not arhiv:
            print("Архив пуст")
            return

        po_prioritetam = {"high": 0, "normal": 0, "low": 0}
        for z in arhiv:
            po_prioritetam[z["priority"]] = po_prioritetam.get(z["priority"], 0) + 1

        print(f"\n{'=' * 40}")
        print(f"  СТАТИСТИКА АРХИВА")
        print(f"{'=' * 40}")
        print(f"  Всего в архиве: {len(arhiv)}")
        print(f"  Высокий приоритет: {po_prioritetam['high']}")
        print(f"  Обычный приоритет: {po_prioritetam['normal']}")
        print(f"  Низкий приоритет:  {po_prioritetam['low']}")
        print(f"{'=' * 40}\n")