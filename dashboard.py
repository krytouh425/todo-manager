# Дашборд — общая сводка по всем задачам команды
# Выводится при запуске приложения как главный экран

from datetime import datetime


class Dashboard:
    def __init__(self, tasks, storage):
        self.tasks = tasks
        self.storage = storage
        self.vremya = datetime.now()

    def _aktivnye(self):
        return [t for t in self.tasks if not t.done]

    def _vypolnennye(self):
        return [t for t in self.tasks if t.done]

    def _srochnye(self):
        return [t for t in self.tasks if t.priority == "high" and not t.done]

    def pokazat(self):
        aktivnye = self._aktivnye()
        vypolnennye = self._vypolnennye()
        srochnye = self._srochnye()
        vsego = len(self.tasks)
        protsent = round(len(vypolnennye) / vsego * 100) if vsego > 0 else 0
        progress = "█" * (protsent // 10) + "░" * (10 - protsent // 10)

        print(f"\n{'=' * 50}")
        print(f"  ДАШБОРД — {self.vremya.strftime('%d.%m.%Y %H:%M')}")
        print(f"{'=' * 50}")
        print(f"  Всего задач:     {vsego}")
        print(f"  В работе:        {len(aktivnye)}")
        print(f"  Выполнено:       {len(vypolnennye)}")
        print(f"  Прогресс:        {progress} {protsent}%")

        # показываем разбивку по приоритетам
        high = len([t for t in aktivnye if t.priority == "high"])
        normal = len([t for t in aktivnye if t.priority == "normal"])
        low = len([t for t in aktivnye if t.priority == "low"])
        print(f"\n  Активные по приоритетам:")
        print(f"    Высокий: {high}")
        print(f"    Обычный: {normal}")
        print(f"    Низкий:  {low}")

        if srochnye:
            print(f"\n  Срочные задачи ({len(srochnye)}):")
            for t in srochnye[:5]:
                print(f"    #{t.id} {t.title}")

        if not aktivnye:
            print(f"\n  ✓ Все задачи выполнены!")

        print(f"{'=' * 50}\n")