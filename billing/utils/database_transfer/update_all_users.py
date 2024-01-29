import csv
import os
import sys

import django
from django.db import transaction
from tqdm import tqdm

current_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(os.path.dirname(current_dir))

if base_path not in sys.path:
    sys.path.append(base_path)

# Установите переменные окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User  # noqa


@transaction.atomic
def create_user_from_csv(csv_filepath):
    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:  # Указываем кодировку файла
        reader = csv.reader(csvfile)

        # Перемещаемся к началу файла и пропускаем заголовок
        next(reader, None)

        # Определите общее количество строк (минус заголовок)
        total_lines = sum(1 for row in csvfile)
        csvfile.seek(0)  # Вернуться к началу файла
        next(reader, None)  # Пропустить заголовок, если он есть

        # Используйте tqdm для создания индикатора прогресса
        for row in tqdm(reader, total=total_lines, desc="Processing users"):
            login = row[5]  # Индекс колонки с логином
            password = row[6]  # Индекс колонки с паролем

            # Используйте get_or_create, чтобы избежать создания дубликатов
            user, created = User.objects.get_or_create(username=login)

            # Если пользователь был создан, установите пароль и сохраните
            if created:
                user.set_password(password)
                user.save()


if __name__ == '__main__':
    # Замените 'path_to_your_file.csv' на путь к вашему файлу CSV
    create_user_from_csv('utils/database_transfer/users_utf.csv')
