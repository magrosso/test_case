import socket
import random

def report_error(mod_name: str, tc_name: str) -> str:
    host_name = socket.gethostname().upper()
    print(f'Report function:\n\tHost: {host_name}\n\tModule: {mod_name}\n\tTest Case: {tc_name}')
    report_key = random.randint(1, 1000)
    return f'LST-{report_key}'