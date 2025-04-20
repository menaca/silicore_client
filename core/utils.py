import socket
import random
import string
import psutil

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def get_ip_address():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Unknown"

def get_mac_address():
    try:
        for iface, snics in psutil.net_if_addrs().items():
            for snic in snics:
                if snic.family == psutil.AF_LINK:
                    return snic.address
        return "Unknown"
    except:
        return "Unknown"
