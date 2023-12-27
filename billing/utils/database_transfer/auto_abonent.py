import csv
import os
import django
import sys
from tqdm import tqdm

current_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(os.path.dirname(current_dir))

if base_path not in sys.path:
    sys.path.append(base_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User  # noqa
from apps.abonents.models import Abonent  # noqa
from apps.groups.models import Group  # noqa


def create_user_from_csv(csv_filepath):
    abonents_to_create = []  # Список для хранения объектов Abonent перед bulk_create
    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Пропустите заголовок, если он есть

        total_lines = (sum(1 for _ in csvfile)) / 3  # Подсчитайте общее количество строк
        csvfile.seek(0)  # Вернуться к началу файла
        next(reader, None)  # Пропустите заголовок, если он есть

        for row in tqdm(reader, total=total_lines, desc="Processing abonents"):
            login = row[5]
            user, _ = User.objects.get_or_create(username=login)
            group_guid = row[8]
            group, _ = Group.objects.get_or_create(group_guid=group_guid)

            abonent = Abonent(
                login=user,
                login_mikrotik=login,
                password=row[6],
                name=row[3],
                account_number=row[4],
                balance=row[7],
                group=group,
                ip_addr=row[9],
                block=True if row[14] in ['0', '1'] else False,
                create_date='2020-10-10' if row[17] == '0000-00-00' else row[17],
                credit=row[19],
                credit_check=row[20],
                email=row[21],
                phone=row[22],
                address=row[23],
                passport=row[24],
                description=row[26],
            )
            abonents_to_create.append(abonent)

        # Создайте всех абонентов одним запросом
        Abonent.objects.bulk_create(abonents_to_create)
        print(f"Created {len(abonents_to_create)} abonents.")


if __name__ == '__main__':
    create_user_from_csv('utils/database_transfer/users_utf.csv')
