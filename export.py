# Модуль экспорта задач — выгружаем данные в разные форматы
# Поддерживает JSON, CSV и TXT для отправки руководству

import json
import csv
import os
from datetime import datetime


class ExportZadach:
    def __init__(self, tasks, export_dir="exports"):
        self.tasks = tasks
        self.export_dir = export_dir
        self._sozdat_papku()

    def _sozdat_papku(self):
        # создаём папку для экспорта если её нет
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def _imya_fayla(self, format):
        # генерируем имя файла с датой и временем
        vremya = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.export_dir, f"tasks_{vremya}.{format}")

    def v_json(self):
        fayl = self._imya_fayla("json")
        with open(fayl, "w", encoding="utf-8") as f:
            json.dump(
                [t.to_dict() for t in self.tasks],
                f,
                ensure_ascii=False,
                indent=2
            )
        print(f"✓ Экспортировано в {fayl}")
        return fayl

    def v_csv(self):
        fayl = self._imya_fayla("csv")
        with open(fayl, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            # заголовок
            writer.writerow(["ID", "Название", "Приоритет", "Статус", "Дата создания"])
            for t in self.tasks:
                writer.writerow([
                    t.id,
                    t.title,
                    t.priority,
                    "выполнено" if t.done else "в работе",
                    t.created_at
                ])
        print(f"✓ Экспортировано в {fayl}")
        return fayl

    def v_txt(self):
        fayl = self._imya_fayla("txt")
        with open(fayl, "w", encoding="utf-8") as f:
            f.write(f"СПИСОК ЗАДАЧ — {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write("=" * 50 + "\n\n")
            for t in self.tasks:
                status = "✓" if t.done else "○"
                f.write(f"[{status}] #{t.id} {t.title}\n")
                f.write(f"     Приоритет: {t.priority} | Создано: {t.created_at}\n\n")
        print(f"✓ Экспортировано в {fayl}")
        return fayl