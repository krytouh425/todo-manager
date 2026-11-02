# Модуль очистки — удаляем старые и ненужные задачи
# Используется для поддержания порядка в списке задач команды

from datetime import datetime


class OchistitelZadach:
    def __init__(self, tasks):
        self.tasks = tasks

    def vypolnennye(self):
        # возвращаем все выполненные задачи
        return [t for t in self.tasks if t.done]

    def starye_vypolnennye(self, dney=30):
        # выполненные задачи старше N дней
        starye = []
        for t in self.tasks:
            if not t.done:
                continue
            try:
                data = datetime.strptime(t.created_at, "%Y-%m-%d %H:%M")
                vozrast = (datetime.now() - data).days
                if vozrast >= dney:
                    starye.append(t)
            except ValueError:
                continue
        return starye

    def udalit_vypolnennye(self, tasks, storage):
        # удаляем выполненные задачи из списка
        ids_udalit = {t.id for t in tasks}
        novye = [t for t in self.tasks if t.id not in ids_udalit]
        storage.save(novye)
        print(f"✓ Удалено задач: {len(tasks)}")
        return novye

    def pokazat_na_udalenie(self, dney=30):
        starye = self.starye_vypolnennye(dney)
        if not starye:
            print(f"Нет выполненных задач старше {dney} дней")
            return []

        print(f"\nВыполненные задачи старше {dney} дней ({len(starye)}):")
        print("-" * 40)
        for t in starye:
            print(f"  #{t.id} {t.title} [{t.created_at}]")
        return starye