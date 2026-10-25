# Модуль резервного копирования — сохраняем копии данных
# Запускается автоматически перед каждым изменением списка задач

import os
import json
import shutil
from datetime import datetime

BACKUP_DIR = "backups"      # папка для резервных копий
MAX_BACKUPS = 10            # максимум хранимых копий


class BackupManager:
    def __init__(self, source_file="tasks.json", backup_dir=BACKUP_DIR):
        self.source_file = source_file
        self.backup_dir = backup_dir
        self._sozdat_papku()

    def _sozdat_papku(self):
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def _imya_backup(self):
        # имя файла резервной копии с временной меткой
        vremya = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.backup_dir, f"tasks_backup_{vremya}.json")

    def sozdat_backup(self):
        # создаём резервную копию перед изменением данных
        if not os.path.exists(self.source_file):
            return None

        backup_fayl = self._imya_backup()
        shutil.copy2(self.source_file, backup_fayl)
        print(f"✓ Резервная копия создана: {backup_fayl}")

        self._udalit_starye()
        return backup_fayl

    def _udalit_starye(self):
        # оставляем только последние MAX_BACKUPS копий
        fayly = sorted([
            f for f in os.listdir(self.backup_dir)
            if f.startswith("tasks_backup_")
        ])

        while len(fayly) > MAX_BACKUPS:
            udalit = os.path.join(self.backup_dir, fayly.pop(0))
            os.remove(udalit)

    def vosstanovit(self, backup_fayl):
        # восстанавливаем данные из резервной копии
        if not os.path.exists(backup_fayl):
            raise FileNotFoundError(f"Резервная копия не найдена: {backup_fayl}")

        shutil.copy2(backup_fayl, self.source_file)
        print(f"✓ Данные восстановлены из: {backup_fayl}")

    def spisok_backup(self):
        # выводим список всех резервных копий
        fayly = sorted([
            f for f in os.listdir(self.backup_dir)
            if f.startswith("tasks_backup_")
        ], reverse=True)

        if not fayly:
            print("Резервных копий нет")
            return []

        print(f"\nРезервные копии ({len(fayly)}):")
        for i, f in enumerate(fayly, 1):
            put = os.path.join(self.backup_dir, f)
            razmer = os.path.getsize(put)
            print(f"  {i}. {f} ({razmer} байт)")

        return fayly