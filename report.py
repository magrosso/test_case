import socket
import random

def report_error(mod_name: str, tc_name: str, priority: int) -> str:
    host_name = socket.gethostname().upper()
    print(f'Report:\n\tHost: {host_name}\n\tModule: {mod_name}\n\tTest Case: {tc_name}\n\tPriority: {priority}')
    report_key = random.randint(1, 1000)
    return f'LST-{report_key}'