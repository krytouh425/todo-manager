# Модуль аналитики — глубокий анализ задач команды
# Используется для ежемесячных отчётов руководству

from datetime import datetime
from collections import Counter


class AnalitikZadach:
    def __init__(self, tasks):
        self.tasks = tasks
        self.vremya = datetime.now()

    def produktivnost_po_dnyam(self):
        # считаем сколько задач создавалось каждый день
        schetchik = Counter()
        for t in self.tasks:
            try:
                data = datetime.strptime(t.created_at, "%Y-%m-%d %H:%M")
                schetchik[data.strftime("%Y-%m-%d")] += 1
            except ValueError:
                continue
        return dict(sorted(schetchik.items()))

    def sredneye_vremya_vypolneniya(self):
        # среднее время от создания до выполнения
        # пока задачи не хранят дату выполнения — возвращаем заглушку
        return "Нет данных о дате выполнения"

    def samye_aktivnye_dni(self, top=3):
        po_dnyam = self.produktivnost_po_dnyam()
        if not po_dnyam:
            return []
        otsortirovannye = sorted(
            po_dnyam.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return otsortirovannye[:top]

    def trend(self):
        # растёт или падает активность
        po_dnyam = self.produktivnost_po_dnyam()
        if len(po_dnyam) < 2:
            return "Недостаточно данных"

        znacheniya = list(po_dnyam.values())
        pervaya_polovina = sum(znacheniya[:len(znacheniya)//2])
        vtoraya_polovina = sum(znacheniya[len(znacheniya)//2:])

        if vtoraya_polovina > pervaya_polovina:
            return "📈 Активность растёт"
        elif vtoraya_polovina < pervaya_polovina:
            return "📉 Активность падает"
        else:
            return "➡️ Активность стабильна"

    def vyvesti(self):
        aktivnye_dni = self.samye_aktivnye_dni()

        print(f"\n{'=' * 50}")
        print(f"  АНАЛИТИКА ЗАДАЧ")
        print(f"  Дата: {self.vremya.strftime('%d.%m.%Y')}")
        print(f"{'=' * 50}")
        print(f"  Всего задач: {len(self.tasks)}")
        print(f"  Тренд: {self.trend()}")

        if aktivnye_dni:
            print(f"\n  Самые активные дни:")
            for den, count in aktivnye_dni:
                print(f"    {den}: {count} задач")

        print(f"{'=' * 50}\n")