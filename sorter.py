# Модуль сортировки задач — упорядочиваем список по разным критериям
# Используется для удобного отображения задач команде

from datetime import datetime

PORYADOK_PRIORITETOV = {"high": 0, "normal": 1, "low": 2}


class SortirovshchikZadach:
    def __init__(self, tasks):
        self.tasks = tasks

    def po_prioritetu(self, obratniy=False):
        # сортируем по приоритету: сначала высокий
        return sorted(
            self.tasks,
            key=lambda t: PORYADOK_PRIORITETOV[t.priority],
            reverse=obratniy
        )

    def po_date_sozdaniya(self, novye_pervye=True):
        # сортируем по дате создания
        return sorted(
            self.tasks,
            key=lambda t: datetime.strptime(t.created_at, "%Y-%m-%d %H:%M"),
            reverse=novye_pervye
        )

    def po_id(self, obratniy=False):
        # сортируем по номеру задачи
        return sorted(self.tasks, key=lambda t: t.id, reverse=obratniy)

    def nevypolnennye_pervye(self):
        # сначала активные потом выполненные
        return sorted(self.tasks, key=lambda t: (t.done, PORYADOK_PRIORITETOV[t.priority]))

    def kombinirovanaya(self):
        # основная сортировка — по статусу, потом приоритету, потом дате
        return sorted(
            self.tasks,
            key=lambda t: (
                t.done,
                PORYADOK_PRIORITETOV[t.priority],
                datetime.strptime(t.created_at, "%Y-%m-%d %H:%M")
            )
        )