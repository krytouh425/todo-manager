# Модуль статистики — анализируем продуктивность команды
# Считаем выполненные задачи, среднее время, загрузку по приоритетам

from datetime import datetime


class AnalizZadach:
    def __init__(self, tasks):
        self.tasks = tasks

    def obshaya_statistika(self):
        vsego = len(self.tasks)
        if vsego == 0:
            return None

        vypolneno = len([t for t in self.tasks if t.done])
        v_rabote = vsego - vypolneno
        protsent = round((vypolneno / vsego) * 100, 1)

        return {
            "vsego": vsego,
            "vypolneno": vypolneno,
            "v_rabote": v_rabote,
            "protsent_vypolneniya": protsent
        }

    def po_prioritetam(self):
        # считаем задачи по каждому приоритету
        rezultat = {}
        for prioritet in ("high", "normal", "low"):
            spisok = [t for t in self.tasks if t.priority == prioritet]
            vypolneno = len([t for t in spisok if t.done])
            rezultat[prioritet] = {
                "vsego": len(spisok),
                "vypolneno": vypolneno,
                "v_rabote": len(spisok) - vypolneno
            }
        return rezultat

    def poslednie_dobavlennye(self, kolichestvo=5):
        # последние добавленные задачи по дате создания
        otsortirovannye = sorted(
            self.tasks,
            key=lambda t: datetime.strptime(t.created_at, "%Y-%m-%d %H:%M"),
            reverse=True
        )
        return otsortirovannye[:kolichestvo]

    def vyvesti_otchet(self):
        stat = self.obshaya_statistika()
        if not stat:
            print("Нет задач для анализа")
            return

        print("\n" + "=" * 45)
        print("  АНАЛИЗ ЗАДАЧ")
        print("=" * 45)
        print(f"  Всего задач:        {stat['vsego']}")
        print(f"  Выполнено:          {stat['vypolneno']}")
        print(f"  В работе:           {stat['v_rabote']}")
        print(f"  Выполнение:         {stat['protsent_vypolneniya']}%")

        print("\n  По приоритетам:")
        nazvaniya = {"high": "Высокий", "normal": "Обычный", "low": "Низкий"}
        for prioritet, danye in self.po_prioritetam().items():
            print(f"    {nazvaniya[prioritet]}: {danye['vsego']} задач, "
                  f"{danye['vypolneno']} выполнено")
        print("=" * 45 + "\n")