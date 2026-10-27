# Модуль напоминаний — проверяем задачи которые давно не закрыты
# Запускается при старте приложения и предупреждает команду

from datetime import datetime


class MenedzherNapominaniy:
    def __init__(self, tasks):
        self.tasks = tasks

    def _vozrast_zadachi(self, task):
        # считаем сколько дней задача висит невыполненной
        try:
            data = datetime.strptime(task.created_at, "%Y-%m-%d %H:%M")
            return (datetime.now() - data).days
        except ValueError:
            return 0

    def prosrochennye(self, dney=3):
        # задачи которые висят дольше N дней
        return [
            (t, self._vozrast_zadachi(t))
            for t in self.tasks
            if not t.done and self._vozrast_zadachi(t) >= dney
        ]

    def srochnye_bez_progressa(self):
        # высокий приоритет и висит больше 1 дня
        return [
            t for t in self.tasks
            if not t.done
            and t.priority == "high"
            and self._vozrast_zadachi(t) >= 1
        ]

    def pokazat_napominaniya(self):
        prosroch = self.prosrochennye()
        srochnye = self.srochnye_bez_progressa()

        if not prosroch and not srochnye:
            print("\n✓ Просроченных задач нет\n")
            return

        if srochnye:
            print("\nСРОЧНЫЕ ЗАДАЧИ БЕЗ ПРОГРЕССА:")
            print("-" * 40)
            for t in srochnye:
                dni = self._vozrast_zadachi(t)
                print(f"  #{t.id} {t.title} — {dni} дн.")

        if prosroch:
            print("\nДАВНО НЕ ЗАКРЫТЫЕ ЗАДАЧИ:")
            print("-" * 40)
            for t, dni in sorted(prosroch, key=lambda x: x[1], reverse=True):
                print(f"  #{t.id} {t.title} — {dni} дн. [{t.priority}]")

        print()