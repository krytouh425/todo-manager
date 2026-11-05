# Модуль команды — назначаем задачи участникам команды
# Используется тимлидом для распределения работы между разработчиками

import json
import os

TEAM_FILE = "team.json"  # файл с данными команды


class MenedzherKomandy:
    def __init__(self, filepath=TEAM_FILE):
        self.filepath = filepath

    def _zagruzit(self):
        if not os.path.exists(self.filepath):
            return {"uchastniki": [], "naznacheniya": {}}
        with open(self.filepath, encoding="utf-8") as f:
            return json.load(f)

    def _sohranit(self, danye):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(danye, f, ensure_ascii=False, indent=2)

    def dobavit_uchastnika(self, imya, rol="developer"):
        danye = self._zagruzit()
        if imya not in danye["uchastniki"]:
            danye["uchastniki"].append({"imya": imya, "rol": rol})
            self._sohranit(danye)
            print(f"✓ Участник '{imya}' добавлен в команду")
        else:
            print(f"Участник '{imya}' уже в команде")

    def naznachit(self, task_id, imya):
        danye = self._zagruzit()
        uchastniki = [u["imya"] for u in danye["uchastniki"]]
        if imya not in uchastniki:
            print(f"Участник '{imya}' не найден в команде")
            return
        danye["naznacheniya"][str(task_id)] = imya
        self._sohranit(danye)
        print(f"✓ Задача #{task_id} назначена на '{imya}'")

    def zadachi_uchastnika(self, imya, tasks):
        danye = self._zagruzit()
        naznachennye_ids = {
            int(task_id)
            for task_id, ispolnitel in danye["naznacheniya"].items()
            if ispolnitel == imya
        }
        return [t for t in tasks if t.id in naznachennye_ids]

    def nagruzka_komandy(self, tasks):
        danye = self._zagruzit()
        nagruzka = {}

        for uchastnik in danye["uchastniki"]:
            imya = uchastnik["imya"]
            zadachi = self.zadachi_uchastnika(imya, tasks)
            aktivnye = [t for t in zadachi if not t.done]
            nagruzka[imya] = {
                "vsego": len(zadachi),
                "aktivnye": len(aktivnye),
                "vypolneno": len(zadachi) - len(aktivnye)
            }

        return nagruzka

    def pokazat_nagruzku(self, tasks):
        nagruzka = self.nagruzka_komandy(tasks)
        if not nagruzka:
            print("Команда пуста")
            return

        print(f"\n{'=' * 45}")
        print(f"  НАГРУЗКА КОМАНДЫ")
        print(f"{'=' * 45}")
        for imya, danye in nagruzka.items():
            print(f"  {imya}:")
            print(f"    Активных: {danye['aktivnye']} | Выполнено: {danye['vypolneno']}")
        print(f"{'=' * 45}\n")