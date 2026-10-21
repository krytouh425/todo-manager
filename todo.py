# Модель задачи — основная единица данных в системе
# Используется всеми модулями приложения

from datetime import datetime


class Task:
    def __init__(self, title, priority="normal"):
        self.id = None  # назначается при сохранении
        self.title = title
        self.priority = priority  # low / normal / high
        self.done = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def mark_done(self):
        self.done = True

    def to_dict(self):
        # конвертируем в словарь для сохранения в JSON
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "done": self.done,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        # восстанавливаем задачу из словаря (при загрузке)
        task = cls(data["title"], data["priority"])
        task.id = data["id"]
        task.done = data["done"]
        task.created_at = data["created_at"]
        return task

    def __repr__(self):
        status = "✓" if self.done else "○"
        return f"[{status}] #{self.id} {self.title} ({self.priority})"


# Модуль хранения задач — читает и пишет данные в JSON-файл
# Все операции с диском проходят через этот класс

import json
import os

STORAGE_FILE = "tasks.json"


class TaskStorage:
    def __init__(self):
        self.filepath = STORAGE_FILE

    def load(self):
        if not os.path.exists(self.filepath):
            return []

        with open(self.filepath, "r", encoding="utf-8") as f:
            raw = json.load(f)

        return [Task.from_dict(item) for item in raw]

    def save(self, tasks):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(
                [task.to_dict() for task in tasks],
                f,
                ensure_ascii=False,
                indent=2
            )

    def get_next_id(self, tasks):
        if not tasks:
            return 1
        return max(task.id for task in tasks) + 1

# CLI-интерфейс — точка входа для работы с задачами из терминала
# Команды: add, list, done

import sys


class TaskManager:
    def __init__(self):
        self.storage = TaskStorage()
        self.tasks = self.storage.load()

    def add_task(self, title, priority="normal"):
        task = Task(title, priority)
        task.id = self.storage.get_next_id(self.tasks)
        self.tasks.append(task)
        self.storage.save(self.tasks)
        print(f"✓ Задача добавлена: [{task.priority}] {task.title}")

    def list_tasks(self, show_done=False):
        # по умолчанию показываем только активные задачи
        filtered = self.tasks if show_done else [t for t in self.tasks if not t.done]

        if not filtered:
            print("Список задач пуст")
            return

        print(f"\n{'='*40}")
        for task in filtered:
            print(task)
        print(f"{'='*40}\n")

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.mark_done()
                self.storage.save(self.tasks)
                print(f"✓ Задача #{task_id} выполнена")
                return

        print(f"Задача #{task_id} не найдена")


def main():
    manager = TaskManager()

    if len(sys.argv) < 2:
        print("Использование: python todo.py [add|list|done] [аргументы]")
        return

    command = sys.argv[1]

    try:
        if command == "add":
            title = validate_title(sys.argv[2] if len(sys.argv) > 2 else "")
            priority = validate_priority(sys.argv[3] if len(sys.argv) > 3 else "normal")
            manager.add_task(title, priority)

        elif command == "list":
            show_done = "--all" in sys.argv
            manager.list_tasks(show_done)

        elif command == "done":
            task_id = validate_task_id(sys.argv[2] if len(sys.argv) > 2 else "")
            manager.complete_task(task_id)

        else:
            print(f"Неизвестная команда: {command}")

    except ValueError as e:
        print(f"Ошибка: {e}")
    except IndexError:
        print("Ошибка: недостаточно аргументов для команды")


if __name__ == "__main__":
    main()


# Вспомогательные функции — валидация входных данных
# Защищаем приложение от кривого ввода пользователя

VALID_PRIORITIES = ("low", "normal", "high")
MAX_TITLE_LENGTH = 100


def validate_priority(priority):
    # если передали неверный приоритет — возвращаем дефолт и предупреждаем
    if priority not in VALID_PRIORITIES:
        print(f"! Неверный приоритет '{priority}', установлен 'normal'")
        return "normal"
    return priority


def validate_title(title):
    title = title.strip()

    if not title:
        raise ValueError("Название задачи не может быть пустым")

    if len(title) > MAX_TITLE_LENGTH:
        raise ValueError(f"Название слишком длинное (максимум {MAX_TITLE_LENGTH} символов)")

    return title


def validate_task_id(raw_id):
    # ловим случай когда пользователь передал не число
    try:
        task_id = int(raw_id)
        if task_id <= 0:
            raise ValueError
        return task_id
    except ValueError:
        raise ValueError(f"ID задачи должен быть положительным числом, получено: '{raw_id}'")

# Фильтрация задач по приоритету — добавлено по запросу команды
# Позволяет быстро найти срочные задачи не листая весь список

class FiltrZadach:
    def __init__(self, tasks):
        self.tasks = tasks

    def po_prioritetu(self, prioritet):
        # возвращаем только задачи с нужным приоритетом
        prioritet = prioritet.lower()
        if prioritet not in ("low", "normal", "high"):
            raise ValueError(f"Неверный приоритет '{prioritet}', доступны: low, normal, high")
        return [t for t in self.tasks if t.priority == prioritet]

    def aktivnye(self):
        # только незавершённые задачи
        return [t for t in self.tasks if not t.done]

    def po_prioritetu_i_statusu(self, prioritet, tolko_aktivnye=True):
        # комбинированный фильтр — приоритет + статус
        otfiltrovannye = self.po_prioritetu(prioritet)
        if tolko_aktivnye:
            otfiltrovannye = [t for t in otfiltrovannye if not t.done]
        return otfiltrovannye

    def vyvesti(self, tasks):
        if not tasks:
            print("Задач не найдено")
            return
        print(f"\n{'=' * 40}")
        for task in tasks:
            print(task)
        print(f"{'=' * 40}\n")