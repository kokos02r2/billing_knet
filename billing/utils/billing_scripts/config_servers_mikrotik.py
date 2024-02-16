import os

from dotenv import load_dotenv

load_dotenv()

SERVERS = {
    "Саваслейка": {
        "host": os.getenv('IP_ADDRESS_SAVA'),
        "username": os.getenv('LOGIN_SAVA'),
        "password": os.getenv('PASSWORD'),
        "port": int(os.getenv('PORT_UNIVERSAL')),
        "remote_ip": False,
        "local_ip": "10.13.0.1",
    },
    "Октябрьский_1": {
        "host": os.getenv('IP_ADDRESS_OKT1'),
        "username": os.getenv('LOGIN'),
        "password": os.getenv('PASSWORD'),
        "port": int(os.getenv('PORT_OKT1')),
        "remote_ip": False,
        "local_ip": "172.16.0.1"
    },
    "Октябрьский_2": {
        "host": os.getenv('IP_ADDRESS_OKT2'),
        "username": os.getenv('LOGIN_OKT2'),
        "password": os.getenv('PASSWORD_OKT2'),
        "port": int(os.getenv('PORT_OKT2')),
        "remote_ip": False,
        "local_ip": "172.16.0.1"
    },
    "ЧистоеБорское": {
        "host": os.getenv('IP_ADDRESS_CHB'),
        "username": os.getenv('LOGIN'),
        "password": os.getenv('PASSWORD'),
        "port": int(os.getenv('PORT_UNIVERSAL')),
        "remote_ip": True,
        "local_ip": "10.12.0.1",
    },
    "Лакша": {
        "host": os.getenv('IP_ADDRESS_LAKSHA'),
        "username": os.getenv('LOGIN'),
        "password": os.getenv('PASSWORD'),
        "port": int(os.getenv('PORT_UNIVERSAL')),
        "remote_ip": True,
        "local_ip": "10.20.0.1",
    },
    "Дуденево_1": {
        "host": os.getenv('IP_ADDRESS_DUD1'),
        "username": os.getenv('LOGIN'),
        "password": os.getenv('PASSWORD'),
        "port": int(os.getenv('PORT_UNIVERSAL')),
        "remote_ip": True,
        "local_ip": "10.12.0.1"
    },
    "Дуденево_2": {
        "host": os.getenv('IP_ADDRESS_DUD2'),
        "username": os.getenv('LOGIN'),
        "password": os.getenv('PASSWORD'),
        "port": int(os.getenv('PORT_UNIVERSAL')),
        "remote_ip": False,
        "local_ip": "10.14.0.1"
    },
    "Останкино": {
        "host": os.getenv('IP_ADDRESS_OST'),
        "username": os.getenv('LOGIN'),
        "password": os.getenv('PASSWORD'),
        "port": int(os.getenv('PORT_OST')),
        "remote_ip": True,
        "local_ip": "10.12.0.1"
    },
    "Боталово": {
        "host": os.getenv('IP_ADDRESS_BOT'),
        "username": os.getenv('LOGIN'),
        "password": os.getenv('PASSWORD'),
        "port": int(os.getenv('PORT_UNIVERSAL')),
        "remote_ip": True,
        "local_ip": "10.10.0.1"
    },
    "Большеорловское": {
        "host": os.getenv('IP_ADDRESS_BO'),
        "username": os.getenv('LOGIN'),
        "password": os.getenv('PASSWORD'),
        "port": int(os.getenv('PORT_TEST')),
        "remote_ip": True,
        "local_ip": "10.12.0.1",
    },
    # "Test": {
    #     "host": os.getenv('IP_ADDRESS_TEST'),
    #     "username": os.getenv('LOGIN'),
    #     "password": os.getenv('PASSWORD'),
    #     "port": int(os.getenv('PORT_TEST')),
    #     "remote_ip": True,
    #     "local_ip": "10.12.0.1",
    # },
}


LETTERS = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D',
        'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
        'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
        'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch',
        'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
        'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }
