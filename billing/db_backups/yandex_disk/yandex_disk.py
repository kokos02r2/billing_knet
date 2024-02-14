import os
import yadisk
import sys
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(os.path.dirname(current_dir))

if base_path not in sys.path:
    sys.path.append(base_path)

from utils.telegram_sender import send_telegram_message # noqa

load_dotenv()


def find_latest_backup(backup_dir):
    """ Найти последний файл бэкапа в директории. """
    files = [f for f in os.listdir(backup_dir) if f.endswith('.bin')]
    if not files:
        raise ValueError(f"No backup files found in directory {backup_dir}")
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(backup_dir, f)))
    return latest_file


def upload_to_yandex_disk(backup_dir, file_name, yandex_token, remote_folder):
    """ Загрузить файл на Яндекс.Диск, если он там отсутствует, и сообщить об ошибках в Telegram. """
    y = yadisk.YaDisk(token=yandex_token)
    remote_path = f"{remote_folder}{file_name}"

    if not y.exists(remote_path):
        y.upload(os.path.join(backup_dir, file_name), remote_path)
        print(f"Uploaded {file_name} to Yandex.Disk")
    else:
        print(f"File {file_name} already exists on Yandex.Disk")


def upload_missing_backups(backup_dir, yandex_token):
    """ Загрузить отсутствующие бэкапы на Яндекс.Диск. """
    y = yadisk.YaDisk(token=yandex_token)
    remote_folder = "/Backup_db_postgres/"

    # Получить список всех файлов в папке на Яндекс.Диске
    remote_files = [item.name for item in y.listdir(remote_folder) if item.type == "file"]

    # Получить список всех локальных файлов бэкапов
    local_files = [f for f in os.listdir(backup_dir) if f.endswith('.bin')]

    # Определить, какие файлы отсутствуют на Яндекс.Диске
    missing_files = [f for f in local_files if f not in remote_files]

    # Загрузить отсутствующие файлы
    for file_name in missing_files:
        upload_to_yandex_disk(backup_dir, file_name, yandex_token, remote_folder)


if __name__ == "__main__":
    yandex_token = os.getenv('YANDEX_TOKEN')
    backup_dir = os.getenv('BACKUP_DIR')
    try:
        upload_missing_backups(backup_dir, yandex_token)
    except Exception as e:
        bot_token = os.getenv('BOT_TOKEN')
        chat_id = os.getenv('CHAT_ID')
        error_message = f"Failed to upload backup file to Yandex.Disk: {e}"
        print(error_message)
        send_telegram_message(bot_token, chat_id, error_message)
