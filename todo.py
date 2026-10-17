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