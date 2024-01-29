import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

import django
import requests
from django.db.models import Prefetch
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(os.path.dirname(current_dir))

if base_path not in sys.path:
    sys.path.append(base_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.abonents.models import Abonent  # noqa
from apps.groups.models import TvIdentifier  # noqa
from utils.billing_scripts.add_users_to_mikrotik import \
    is_message_logged  # noqa
from utils.telegram_sender import send_telegram_message  # noqa

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
LOG_FILE_PATH = "utils/lifestream/lifestream.log"

handler = TimedRotatingFileHandler(
    LOG_FILE_PATH,
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


def call_api(endpoint='', method='get', data=None, params=None, headers=None):
    base_api_url = os.getenv('BASE_API_LIFESTREAM_URL')
    url = f"{base_api_url}/{endpoint}"
    try:
        if method == 'post':
            response = requests.post(base_api_url, json=data, headers=headers)
        elif method == 'delete':
            response = requests.delete(url, headers=headers)
        else:
            response = requests.get(base_api_url, params=params, headers=headers)

        response.raise_for_status()
        return response.json() if response.content else None
    except requests.exceptions.RequestException as err:
        error_message = f"API lifestream request error: {err}"
        if not is_message_logged(LOG_FILE_PATH, error_message):
            send_telegram_message(BOT_TOKEN, CHAT_ID, error_message)
        else:
            logger.info(
                "Repeated occurrence of a known error for the lifestream script. Message in telegram not sent."
            )
        logger.error(error_message)
        return None


def delete_user(api_user):
    try:
        response = call_api(api_user['id'], method='delete')
        logger.info(f"User deleted {api_user['username']}: {response}")
    except requests.exceptions.RequestException as err:
        logger.error(f"Error deleting user {api_user['username']}: {err}")


def create_user(user, tv_ids):
    data = {
            "username": user.login_mikrotik,
            "email": user.email,
            "purchases": tv_ids,
            "password": user.password
    }
    try:
        response = call_api(method='post', data=data)
        logger.info(f"User created {user.login_mikrotik}: {response}")
    except requests.exceptions.RequestException as err:
        logger.error(f"Error creating user {user.login_mikrotik}: {err}")


def process_users(users_with_balance, existing_users):
    for user in users_with_balance:
        existing_user = next((u for u in existing_users if u['username'] == user.login_mikrotik), None)
        tv_ids = [tv.identifier for tv in user.group.tv_identifiers.all()]
        if not existing_user:
            create_user(user, tv_ids)
        else:
            extracted_ids = [d['id'] for d in existing_user['subscriptions']]
            if set(extracted_ids) != set(tv_ids):
                delete_user(existing_user)
                create_user(user, tv_ids)


def add_user_lifestream():
    tv_identifier_query = TvIdentifier.objects.all()
    group_prefetch = Prefetch('group__tv_identifiers', queryset=tv_identifier_query)

    users_with_positive_balance = Abonent.objects.filter(
        balance__gt=0, group__tv_identifiers__isnull=False
    ).prefetch_related(group_prefetch).distinct()

    all_users_response = call_api()
    if all_users_response:
        existing_users = [{
            'username': user['username'],
            'id': user['id'],
            'subscriptions': user['subscriptions']
        } for user in all_users_response['accounts']]
        positive_balance_logins = [user.login_mikrotik for user in users_with_positive_balance]

        process_users(users_with_positive_balance, existing_users)

        for api_user in all_users_response['accounts']:
            if api_user['username'] not in positive_balance_logins:
                delete_user(api_user)


if __name__ == '__main__':
    logger.info("Start script lifestream")
    try:
        add_user_lifestream()
    except Exception as e:
        error_message = f"Error in the lifestream script: {e}"
        send_telegram_message(BOT_TOKEN, CHAT_ID, error_message)
        logger.error(error_message)
    logger.info("Finish script lifestream")
