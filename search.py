# Модуль поиска задач — быстрый поиск по названию и фильтрам
# Используется когда список задач большой и нужно быстро найти нужную

class PoiskZadach:
    def __init__(self, tasks):
        self.tasks = tasks

    def po_nazvaniyu(self, zapros):
        # ищем по частичному совпадению в названии
        zapros = zapros.lower().strip()
        return [t for t in self.tasks if zapros in t.title.lower()]

    def po_neskol_slovam(self, zapros):
        # все слова запроса должны быть в названии
        slova = zapros.lower().strip().split()
        rezultat = []
        for t in self.tasks:
            nazvanie = t.title.lower()
            if all(slovo in nazvanie for slovo in slova):
                rezultat.append(t)
        return rezultat

    def aktivnye_s_prioritetom(self, prioritet):
        # активные задачи с конкретным приоритетом
        return [
            t for t in self.tasks
            if not t.done and t.priority == prioritet
        ]

    def poslednie(self, kolichestvo=10):
        # последние добавленные задачи
        return sorted(
            self.tasks,
            key=lambda t: t.id,
            reverse=True
        )[:kolichestvo]

    def vyvesti_rezultaty(self, tasks, zapros=""):
        if not tasks:
            print(f"По запросу '{zapros}' ничего не найдено")
            return

        print(f"\n{'=' * 40}")
        print(f"  Найдено: {len(tasks)} задач")
        print(f"{'=' * 40}")
        for t in tasks:
            status = "✓" if t.done else "○"
            print(f"  [{status}] #{t.id} {t.title} [{t.priority}]")
        print(f"{'=' * 40}\n")
