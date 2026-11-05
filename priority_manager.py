# Модуль управления приоритетами — меняем приоритеты задач пакетно
# Используется когда меняются сроки и нужно пересмотреть очередь

from datetime import datetime

PORYADOK = {"high": 0, "normal": 1, "low": 2}


class MenedzherPrioritetov:
    def __init__(self, tasks, storage):
        self.tasks = tasks
        self.storage = storage

    def povysit(self, task_id):
        # повышаем приоритет на один уровень
        for t in self.tasks:
            if t.id == task_id:
                if t.priority == "low":
                    t.priority = "normal"
                elif t.priority == "normal":
                    t.priority = "high"
                else:
                    print(f"Задача #{task_id} уже имеет высший приоритет")
                    return
                self.storage.save(self.tasks)
                print(f"✓ Приоритет задачи #{task_id} повышен до '{t.priority}'")
                return
        print(f"Задача #{task_id} не найдена")

    def ponizit(self, task_id):
        # понижаем приоритет на один уровень
        for t in self.tasks:
            if t.id == task_id:
                if t.priority == "high":
                    t.priority = "normal"
                elif t.priority == "normal":
                    t.priority = "low"
                else:
                    print(f"Задача #{task_id} уже имеет низший приоритет")
                    return
                self.storage.save(self.tasks)
                print(f"✓ Приоритет задачи #{task_id} понижен до '{t.priority}'")
                return
        print(f"Задача #{task_id} не найдена")

    def vse_na_normal(self):
        # сбрасываем все приоритеты до normal
        izmeneno = 0
        for t in self.tasks:
            if t.priority != "normal":
                t.priority = "normal"
                izmeneno += 1
        self.storage.save(self.tasks)
        print(f"✓ Сброшено приоритетов: {izmeneno}")