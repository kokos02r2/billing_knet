import csv
import os
import django
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(os.path.dirname(current_dir))

if base_path not in sys.path:
    sys.path.append(base_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.groups.models import Group # noqa


def create_user_from_csv(csv_filepath):
    with open(csv_filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            group_name = row[3]
            bandwidth = row[5]
            month_price = row[6]
            group_guid = row[0]
            Group.objects.get_or_create(
                group_name=group_name,
                bandwidth=bandwidth,
                month_price=month_price,
                group_guid=group_guid
            )


if __name__ == '__main__':
    create_user_from_csv('utils/database_transfer/csv/updated_file_with_positive_balance.csv')
