import csv
import os
import django
import sys
from tqdm import tqdm
from django.contrib.auth.hashers import make_password

current_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(os.path.dirname(current_dir))

if base_path not in sys.path:
    sys.path.append(base_path)

# Установите переменные окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User # noqa


def create_user_from_csv(csv_filepath):
    users_to_create = []  # Список для сбора пользователей перед bulk_create

    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Пропустите заголовок

        existing_usernames = set(User.objects.values_list('username', flat=True))  # Получите существующие имена пользователей

        # Определите общее количество строк
        total_lines = sum(1 for _ in csvfile)
        csvfile.seek(0)
        next(reader, None)

        for row in tqdm(reader, total=total_lines, desc="Preparing user data"):
            login = row[5]
            password = row[6]

            # Пропускайте пользователей, которые уже существуют
            if login not in existing_usernames:
                # Подготовьте пользователя для создания
                user = User(username=login)
                user.password = make_password(password)  # Хэшируйте пароль перед сохранением
                users_to_create.append(user)
                existing_usernames.add(login)  # Добавьте нового пользователя в существующие имена

        # Создайте всех пользователей одним запросом
        User.objects.bulk_create(users_to_create)
        print(f"Created {len(users_to_create)} users.")


if __name__ == '__main__':
    create_user_from_csv('utils/database_transfer/csv/users_utf.csv')
