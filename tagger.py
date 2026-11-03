# Модуль меток — добавляем теги к задачам для гибкой фильтрации
# По запросу команды — issue #3 "Добавить поддержку меток для задач"

import json
import os

TAGS_FILE = "tags.json"  # файл с метками задач


class MenedzherMetok:
    def __init__(self, filepath=TAGS_FILE):
        self.filepath = filepath

    def _zagruzit(self):
        if not os.path.exists(self.filepath):
            return {}
        with open(self.filepath, encoding="utf-8") as f:
            return json.load(f)

    def _sohranit(self, danye):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(danye, f, ensure_ascii=False, indent=2)

    def dobavit_metku(self, task_id, metka):
        # добавляем метку к задаче
        danye = self._zagruzit()
        klyuch = str(task_id)
        if klyuch not in danye:
            danye[klyuch] = []
        if metka not in danye[klyuch]:
            danye[klyuch].append(metka)
            self._sohranit(danye)
            print(f"✓ Метка '{metka}' добавлена к задаче #{task_id}")
        else:
            print(f"Метка '{metka}' уже есть у задачи #{task_id}")

    def udalit_metku(self, task_id, metka):
        danye = self._zagruzit()
        klyuch = str(task_id)
        if klyuch in danye and metka in danye[klyuch]:
            danye[klyuch].remove(metka)
            self._sohranit(danye)
            print(f"✓ Метка '{metka}' удалена с задачи #{task_id}")

    def metki_zadachi(self, task_id):
        danye = self._zagruzit()
        return danye.get(str(task_id), [])

    def zadachi_po_metke(self, metka):
        # находим все задачи с нужной меткой
        danye = self._zagruzit()
        return [
            int(task_id)
            for task_id, metki in danye.items()
            if metka in metki
        ]

    def vse_metki(self):
        # возвращаем все уникальные метки
        danye = self._zagruzit()
        metki = set()
        for spisok in danye.values():
            metki.update(spisok)
        return sorted(metki)