# Модуль отчётов — формируем итоговый отчёт по задачам команды
# Используется руководителем для контроля работы отдела

from datetime import datetime


class ReporterZadach:
    def __init__(self, tasks):
        self.tasks = tasks
        self.vremya = datetime.now()

    def _statistika(self):
        vsego = len(self.tasks)
        vypolneno = len([t for t in self.tasks if t.done])
        v_rabote = vsego - vypolneno
        protsent = round(vypolneno / vsego * 100, 1) if vsego > 0 else 0

        po_prioritetam = {"high": 0, "normal": 0, "low": 0}
        for t in self.tasks:
            po_prioritetam[t.priority] += 1

        return {
            "vsego": vsego,
            "vypolneno": vypolneno,
            "v_rabote": v_rabote,
            "protsent": protsent,
            "po_prioritetam": po_prioritetam
        }

    def kratkiy(self):
        # краткий отчёт для быстрого просмотра
        stat = self._statistika()
        print(f"\n{'=' * 40}")
        print(f"  ЗАДАЧИ — {self.vremya.strftime('%d.%m.%Y')}")
        print(f"{'=' * 40}")
        print(f"  Всего:      {stat['vsego']}")
        print(f"  Выполнено:  {stat['vypolneno']} ({stat['protsent']}%)")
        print(f"  В работе:   {stat['v_rabote']}")
        print(f"{'=' * 40}\n")

    def polnyy(self):
        # полный отчёт с деталями по приоритетам
        stat = self._statistika()
        nazvaniya = {"high": "Высокий", "normal": "Обычный", "low": "Низкий"}

        print(f"\n{'=' * 45}")
        print(f"  ПОЛНЫЙ ОТЧЁТ ПО ЗАДАЧАМ")
        print(f"  Дата: {self.vremya.strftime('%d.%m.%Y %H:%M')}")
        print(f"{'=' * 45}")
        print(f"  Всего задач:     {stat['vsego']}")
        print(f"  Выполнено:       {stat['vypolneno']} ({stat['protsent']}%)")
        print(f"  В работе:        {stat['v_rabote']}")
        print(f"\n  По приоритетам:")
        for prioritet, kolichestvo in stat["po_prioritetam"].items():
            print(f"    {nazvaniya[prioritet]}: {kolichestvo}")

        nevypolnennye_high = [
            t for t in self.tasks
            if not t.done and t.priority == "high"
        ]
        if nevypolnennye_high:
            print(f"\n  Срочные невыполненные ({len(nevypolnennye_high)}):")
            for t in nevypolnennye_high:
                print(f"    #{t.id} {t.title}")
        print(f"{'=' * 45}\n")