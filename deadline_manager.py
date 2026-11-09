# Модуль дедлайнов — контролируем сроки выполнения задач
# По запросу команды — issue #2 "Добавить дедлайн для задач"

import json
import os
from datetime import datetime

DEADLINES_FILE = "deadlines.json"  # файл с дедлайнами


class MenedzherDedlaynov:
    def __init__(self, filepath=DEADLINES_FILE):
        self.filepath = filepath

    def _zagruzit(self):
        if not os.path.exists(self.filepath):
            return {}
        with open(self.filepath, encoding="utf-8") as f:
            return json.load(f)

    def _sohranit(self, danye):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(danye, f, ensure_ascii=False, indent=2)

    def ustanovit(self, task_id, data_str):
        # устанавливаем дедлайн для задачи
        try:
            datetime.strptime(data_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Неверный формат даты '{data_str}', используй ГГГГ-ММ-ДД")

        danye = self._zagruzit()
        danye[str(task_id)] = data_str
        self._sohranit(danye)
        print(f"✓ Дедлайн задачи #{task_id} установлен на {data_str}")

    def poluchit(self, task_id):
        danye = self._zagruzit()
        return danye.get(str(task_id))

    def prosrochennye(self, tasks):
        # задачи у которых истёк дедлайн
        danye = self._zagruzit()
        segodnya = datetime.now().date()
        rezultat = []

        for t in tasks:
            if t.done:
                continue
            dedlayn_str = danye.get(str(t.id))
            if not dedlayn_str:
                continue
            dedlayn = datetime.strptime(dedlayn_str, "%Y-%m-%d").date()
            if dedlayn < segodnya:
                rezultat.append((t, dedlayn_str))

        return rezultat

    def skoro_istekayut(self, tasks, dney=3):
        # дедлайны которые истекают в ближайшие N дней
        danye = self._zagruzit()
        segodnya = datetime.now().date()
        rezultat = []

        for t in tasks:
            if t.done:
                continue
            dedlayn_str = danye.get(str(t.id))
            if not dedlayn_str:
                continue
            dedlayn = datetime.strptime(dedlayn_str, "%Y-%m-%d").date()
            raznitsa = (dedlayn - segodnya).days
            if 0 <= raznitsa <= dney:
                rezultat.append((t, dedlayn_str, raznitsa))

        return rezultat

    def pokazat_vse(self, tasks):
        danye = self._zagruzit()
        if not danye:
            print("Дедлайны не установлены")
            return

        segodnya = datetime.now().date()
        prosrochennye = self.prosrochennye(tasks)
        prosrochennye_ids = {t.id for t, _ in prosrochennye}

        print(f"\n{'=' * 45}")
        print(f"  ДЕДЛАЙНЫ ЗАДАЧ — {segodnya.strftime('%d.%m.%Y')}")
        print(f"{'=' * 45}")
        for t in tasks:
            dedlayn = danye.get(str(t.id))
            if dedlayn:
                status = "✓" if t.done else "○"
                prosroch = " ⚠️ ПРОСРОЧЕНО" if t.id in prosrochennye_ids else ""
                print(f"  [{status}] #{t.id} {t.title} — до {dedlayn}{prosroch}")
        print(f"{'=' * 45}\n")