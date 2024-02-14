import random

from apps.abonents.models import Abonent


def generate_random_ip():
    return '.'.join(map(str, (random.randint(0, 255) for _ in range(4))))


def get_all_used_ips():
    return list(Abonent.objects.values_list('ip_addr', flat=True))


def generate_unique_ip():
    used_ips = set(get_all_used_ips())
    while True:
        random_ip = generate_random_ip()
        if random_ip not in used_ips:
            used_ips.add(random_ip)
            return random_ip
