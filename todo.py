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