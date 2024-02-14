import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from logging.handlers import TimedRotatingFileHandler
from django.db.models import Q

import django
from dotenv import load_dotenv
from routeros_api import RouterOsApiPool

current_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(os.path.dirname(current_dir))

if base_path not in sys.path:
    sys.path.append(base_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.abonents.models import Abonent  # noqa
from apps.groups.models import Group  # noqa
from utils.billing_scripts.config_servers_mikrotik import LETTERS  # noqa
from utils.billing_scripts.config_servers_mikrotik import SERVERS  # noqa
from utils.telegram_sender import send_telegram_message  # noqa

load_dotenv()

handler = TimedRotatingFileHandler(
    'billing_knet/billing/utils/billing_scripts/logs/mikrotik_connection_errors.log',
    when='midnight',
    backupCount=0,
    encoding='utf-8'
)

handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
))

handler.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def transliterate(name):
    translit_name = ''
    for char in name:
        translit_name += LETTERS.get(char, char)
    return translit_name


def is_message_logged(log_file_path, message):
    try:
        with open(log_file_path, 'r') as log_file:
            # Проверить каждую строку в файле на наличие сообщения
            for line in log_file:
                if message in line:
                    return True
    except FileNotFoundError:
        # Если файл не найден, значит сообщения точно нет
        return False
    return False


def process_user(user, existing_users, existing_users_data, server_settings):
    try:
        local_api = RouterOsApiPool(server_settings["host"], username=server_settings["username"],
                                    password=server_settings["password"], port=server_settings["port"]).get_api()
        user_str = str(user.login_mikrotik)
        comment = transliterate(str(user.name))
        if user.ip_addr is None:
            print(f"Skipping user {user.login}: no IP address.")
            return
        params = {
                    "name": user_str,
                    "password": str(user.password),
                    "comment": comment,
                    "profile": str(user.group.bandwidth)
                }
        if server_settings["remote_ip"]:
            params["remote_address"] = str(user.ip_addr)
        if user_str in existing_users:
            if server_settings["remote_ip"] and not existing_users_data[user_str].get('remote-address'):
                existing_users_data_id = existing_users_data[user_str].get('id')
                local_api.get_resource('/ppp/secret').set(id=existing_users_data_id, remote_address=str(user.ip_addr))
            if not server_settings["remote_ip"] and existing_users_data[user_str].get('remote-address'):
                existing_users_data_id = existing_users_data[user_str].get('id')
                local_api.get_resource('/ppp/secret').remove(id=existing_users_data_id)
                local_api.get_resource('/ppp/secret').add(**params)
            if server_settings["remote_ip"] and existing_users_data[user_str].get('remote-address'):
                if (existing_users_data[user_str].get('password') != str(user.password) or
                    existing_users_data[user_str].get('name') != str(user.login_mikrotik) or
                    existing_users_data[user_str].get('profile') != str(user.group.bandwidth) or
                    existing_users_data[user_str].get('comment') != comment or
                    existing_users_data[user_str].get('remote-address') != str(user.ip_addr)):
                    existing_users_data_id = existing_users_data[user_str].get('id')
                    local_api.get_resource('/ppp/secret').remove(id=existing_users_data_id)
                    local_api.get_resource('/ppp/secret').add(**params)
            if not server_settings["remote_ip"] and not existing_users_data[user_str].get('remote-address'):
                if (existing_users_data[user_str].get('password') != str(user.password) or
                    existing_users_data[user_str].get('name') != str(user.login_mikrotik) or
                    existing_users_data[user_str].get('comment') != comment or
                    existing_users_data[user_str].get('profile') != str(user.group.bandwidth)):
                    existing_users_data_id = existing_users_data[user_str].get('id')
                    local_api.get_resource('/ppp/secret').remove(id=existing_users_data_id)
                    local_api.get_resource('/ppp/secret').add(**params)
        else:
            print(f"Creating user {user.login}")
            local_api.get_resource('/ppp/secret').add(**params)
    except Exception as e:
        print(f"Произошла ошибка при обработке пользователя {user.login_mikrotik}: {e}")
    finally:
        local_api.disconnect()


def process_user_delete(user_login, server_settings):
    try:
        local_api = RouterOsApiPool(server_settings["host"], username=server_settings["username"],
                                    password=server_settings["password"], port=server_settings["port"]).get_api()
        print(f"Deleting user {user_login}")
        user_data = local_api.get_resource('/ppp/secret').get(name=user_login)[0]
        local_api.get_resource('/ppp/secret').remove(id=user_data['id'])
        active_user_data = local_api.get_resource('/ppp/active').get(name=user_login)[0]
        local_api.get_resource('/ppp/active').remove(id=active_user_data['id'])
    except Exception as e:
        print(f"Произошла ошибка при обработке пользователя {user_login}: {e}")
    finally:
        local_api.disconnect()


def create_missing_profiles(server_settings):
    try:
        logger.info(f'Попытка подключения к серверу {server_settings["host"]}')
        connection = RouterOsApiPool(server_settings["host"], username=server_settings["username"],
                                     password=server_settings["password"], port=server_settings["port"])
        api = connection.get_api()
        existing_profiles = set(profile['name'] for profile in api.get_resource('/ppp/profile').get())
        groups = Group.objects.all()
        unique_bandwidths = set(group.bandwidth for group in groups)

        for bandwidth in unique_bandwidths:
            in_rate, out_rate = bandwidth.split('/')
            rate_limit = f"{int(in_rate) * 1000}/{int(out_rate) * 1000}"

            if bandwidth not in existing_profiles:
                print(f"Creating PPP profile with bandwidth {bandwidth}")
                api.get_resource('/ppp/profile').add(
                    name=bandwidth,
                    rate_limit=rate_limit,
                    only_one='yes',
                    local_address=server_settings["local_ip"]
                )
        users_with_positive_balance = Abonent.objects.filter(
            Q(balance__gte=0) & Q(block=False)
        )
        existing_users_data = {user['name']: user for user in api.get_resource('/ppp/secret').get()}
        existing_users = set(existing_users_data.keys())
        with ThreadPoolExecutor(max_workers=50) as executor:
            for user in users_with_positive_balance:
                executor.submit(process_user, user, existing_users, existing_users_data, server_settings)

        existing_users_data = {user['name']: user for user in api.get_resource('/ppp/secret').get()}
        existing_users = set(existing_users_data.keys())
        db_users_negative_balance_logins = set(Abonent.objects.filter(
            Q(balance__lt=0) | Q(block=True)
        ).values_list('login_mikrotik', flat=True))
        users_to_delete = existing_users.intersection(db_users_negative_balance_logins)
        while True:
            with ThreadPoolExecutor(max_workers=20) as executor:
                for user_login in users_to_delete:
                    executor.submit(process_user_delete, user_login, server_settings)
            existing_users_data = {user['name']: user for user in api.get_resource('/ppp/secret').get()}
            existing_users = set(existing_users_data.keys())
            db_users_negative_balance_logins = set(Abonent.objects.filter(
                Q(balance__lt=0) | Q(block=True)
            ).values_list('login_mikrotik', flat=True))
            users_to_delete = existing_users.intersection(db_users_negative_balance_logins)
            if not users_to_delete:
                break
        all_positive_db_users = set(Abonent.objects.filter(balance__gte=0).values_list('login_mikrotik', flat=True))
        error_users = existing_users - all_positive_db_users
        for error_user in error_users:
            existing_users_data_id = existing_users_data[error_user].get('id')
            api.get_resource('/ppp/secret').remove(id=existing_users_data_id)
        logger.info(f'Успешно подключен к серверу {server_settings["host"]}')
    except Exception as e:
        logger.error(f'Не удалось подключиться к серверу {server_settings["host"]}: {e}')
        raise
    finally:
        connection.disconnect()


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for server_name, server_settings in SERVERS.items():
            future = executor.submit(create_missing_profiles, server_settings)
            futures.append((server_name, future))

        log_file_path = 'billing_knet/billing/utils/billing_scripts/logs/mikrotik_connection_errors.log'  # Укажите путь к вашему файлу лога

        for server_name, future in futures:
            try:
                future.result()
            except Exception as e:
                error_message = f"Ошибка при добавлении пользователей на сервер {server_name}: {e}"

                # Проверьте, было ли уже залогировано такое же сообщение
                if not is_message_logged(log_file_path, error_message):
                    logger.error(error_message)
                    bot_token = os.getenv('BOT_TOKEN')
                    chat_id = os.getenv('CHAT_ID')
                    send_telegram_message(bot_token, chat_id, error_message)
                else:
                    # Если сообщение уже есть в логе, просто залогируйте факт его возникновения
                    logger.info(f"Повторное возникновение известной ошибки для сервера {server_name}. Сообщение не отправлено.")
