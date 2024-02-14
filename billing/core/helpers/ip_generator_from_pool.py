import random

from core.helpers.constants import ECONOM_LIST, MAXIMUM_LIST, OPTIMUM_LIST
from apps.abonents.models import Abonent


def generate_ip_from_range(start_ip, end_ip):
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    return ".".join(map(str, (random.randint(start[i], end[i]) for i in range(4))))


def get_all_used_ips():
    return list(Abonent.objects.values_list('ip_addr', flat=True))


def generate_unique_ip_from_range(tarif, contract):
    if 887000 <= contract <= 887200:
        if tarif in ECONOM_LIST:
            ip_range_start = '10.12.40.1'
            ip_range_end = '10.12.40.254'
        elif tarif in OPTIMUM_LIST:
            ip_range_start = '10.12.41.1'
            ip_range_end = '10.12.41.254'
        elif tarif in MAXIMUM_LIST:
            ip_range_start = '10.12.42.1'
            ip_range_end = '10.12.42.254'
        else:
            raise ValueError("Неизвестный тариф")

    if 887500 <= contract <= 887999:
        if tarif in ECONOM_LIST:
            ip_range_start = '10.20.11.1'
            ip_range_end = '10.20.11.254'
        elif tarif in OPTIMUM_LIST:
            ip_range_start = '10.20.12.1'
            ip_range_end = '10.20.12.254'
        elif tarif in MAXIMUM_LIST:
            ip_range_start = '10.20.13.1'
            ip_range_end = '10.20.13.254'
        else:
            raise ValueError("Неизвестный тариф")

    if 883700 <= contract <= 883799 or 883400 <= contract <= 883499 or 886000 <= contract <= 886400:
        if tarif in ECONOM_LIST:
            ip_range_start = '10.12.55.1'
            ip_range_end = '10.12.55.254'
        elif tarif in OPTIMUM_LIST:
            ip_range_start = '10.12.56.1'
            ip_range_end = '10.12.56.254'
        elif tarif in MAXIMUM_LIST:
            ip_range_start = '10.12.57.1'
            ip_range_end = '10.12.57.254'
        else:
            raise ValueError("Неизвестный тариф")

    if 884000 <= contract <= 884300:
        if tarif in ECONOM_LIST:
            ip_range_start = '10.12.15.1'
            ip_range_end = '10.12.15.254'
        elif tarif in OPTIMUM_LIST:
            ip_range_start = '10.12.16.1'
            ip_range_end = '10.12.16.254'
        elif tarif in MAXIMUM_LIST:
            ip_range_start = '10.12.17.1'
            ip_range_end = '10.12.17.254'
        else:
            raise ValueError("Неизвестный тариф")

    if 889100 <= contract <= 889299:
        if tarif in ECONOM_LIST:
            ip_range_start = '10.10.40.1'
            ip_range_end = '10.10.40.254'
        elif tarif in OPTIMUM_LIST:
            ip_range_start = '10.10.41.1'
            ip_range_end = '10.10.41.254'
        elif tarif in MAXIMUM_LIST:
            ip_range_start = '10.10.42.1'
            ip_range_end = '10.10.42.254'
        else:
            raise ValueError("Неизвестный тариф")

    if 885000 <= contract <= 885399:
        if tarif in ECONOM_LIST:
            ip_range_start = '10.12.10.1'
            ip_range_end = '10.12.10.254'
        elif tarif in OPTIMUM_LIST:
            ip_range_start = '10.12.11.1'
            ip_range_end = '10.12.11.254'
        elif tarif in MAXIMUM_LIST:
            ip_range_start = '10.12.12.1'
            ip_range_end = '10.12.12.254'
        else:
            raise ValueError("Неизвестный тариф")

    used_ips = set(get_all_used_ips())
    while True:
        unique_ip = generate_ip_from_range(ip_range_start, ip_range_end)
        if unique_ip not in used_ips:
            used_ips.add(unique_ip)
            return unique_ip
