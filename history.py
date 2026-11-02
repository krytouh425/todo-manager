# Модуль истории — отслеживаем все изменения задач
# Позволяет увидеть кто и когда менял задачи

from datetime import datetime


class HistoryManager:
    def __init__(self, filepath="history.log"):
        self.filepath = filepath

    def zapisat(self, deystvie, task, detali=""):
        # записываем действие с задачей
        vremya = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stroka = f"{vremya} | {deystvie} | #{task.id} '{task.title}'"
        if detali:
            stroka += f" | {detali}"

        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(stroka + "\n")

    def prochitat(self, poslednie=50):
        # читаем последние N записей истории
        try:
            with open(self.filepath, encoding="utf-8") as f:
                stroki = f.readlines()
            return [s.strip() for s in stroki[-poslednie:]]
        except FileNotFoundError:
            return []

    def po_zadache(self, task_id):
        # история конкретной задачи
        vse = self.prochitat(poslednie=1000)
        return [s for s in vse if f"#{task_id} " in s]

    def vyvesti(self, poslednie=20):
        zapisi = self.prochitat(poslednie)
        if not zapisi:
            print("История пуста")
            return

        print(f"\n{'=' * 50}")
        print(f"  ИСТОРИЯ ИЗМЕНЕНИЙ (последние {poslednie})")
        print(f"{'=' * 50}")
        for zapis in zapisi:
            print(f"  {zapis}")
        print(f"{'=' * 50}\n")