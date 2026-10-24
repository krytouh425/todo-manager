# Модуль уведомлений — оповещаем о срочных задачах
# Проверяет задачи с высоким приоритетом и напоминает о них

from datetime import datetime


class MenedzherUvedomleniy:
    def __init__(self, tasks):
        self.tasks = tasks

    def srochnye_zadachi(self):
        # возвращаем все невыполненные задачи с высоким приоритетом
        return [t for t in self.tasks if t.priority == "high" and not t.done]

    def davnie_zadachi(self, dney=7):
        # задачи которые висят больше N дней
        davnie = []
        for t in self.tasks:
            if t.done:
                continue
            try:
                data = datetime.strptime(t.created_at, "%Y-%m-%d %H:%M")
                raznitsa = (datetime.now() - data).days
                if raznitsa >= dney:
                    davnie.append((t, raznitsa))
            except ValueError:
                continue
        return davnie

    def pokazat_uvedomleniya(self):
        srochnye = self.srochnye_zadachi()
        davnie = self.davnie_zadachi()

        est_uvedomleniya = False

        if srochnye:
            est_uvedomleniya = True
            print("\n⚠️  СРОЧНЫЕ ЗАДАЧИ:")
            print("-" * 40)
            for t in srochnye:
                print(f"  #{t.id} {t.title}")

        if davnie:
            est_uvedomleniya = True
            print("\n⏰  ДАВНО НЕ ВЫПОЛНЕНЫ:")
            print("-" * 40)
            for t, dney in davnie:
                print(f"  #{t.id} {t.title} — {dney} дней")

        if not est_uvedomleniya:
            print("\n✓ Срочных уведомлений нет")

        print()

    def kolichestvo_srochnykh(self):
        return len(self.srochnye_zadachi())