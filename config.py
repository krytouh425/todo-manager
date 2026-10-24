# Конфигурация приложения — все настройки в одном месте
# Меняй здесь, не трогая основной код

# настройки хранения задач
STORAGE_FILE = "tasks.json"
MAX_TASKS = 1000  # максимум задач в списке

# настройки приоритетов
DEFAULT_PRIORITY = "normal"
VALID_PRIORITIES = ("low", "normal", "high")

# настройки вывода
DATE_FORMAT = "%Y-%m-%d %H:%M"
MAX_TITLE_LENGTH = 100

# настройки экспорта
EXPORT_DIR = "exports"  # папка для экспортированных файлов
EXPORT_FORMATS = ("json", "csv", "txt")