import platform
import psutil
from datetime import datetime
import cpuinfo
from .utils import get_ip_address, get_mac_address
import pyautogui

def get_screen_resolution():
    try:
        width, height = pyautogui.size()
        return f"{width}x{height}"
    except:
        return "Unknown"

def get_system_info():
    cpu = cpuinfo.get_cpu_info()
    battery = psutil.sensors_battery()

    return {
        "computer_name": platform.node(),
        "os": f"{platform.system()} {platform.release()}",
        "timestamp": datetime.now().isoformat(),
        "status": "online",

        "cpu": {
            "brand": cpu.get("brand_raw", "Unknown"),
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "frequency": cpu.get("hz_advertised_friendly", "Unknown"),
            "usage_percent": psutil.cpu_percent(interval=1)
        },

        "ram": {
            "total_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
            "used_gb": round(psutil.virtual_memory().used / (1024 ** 3), 2),
            "usage_percent": psutil.virtual_memory().percent
        },

        "disk": {
            "total_gb": round(psutil.disk_usage('/').total / (1024 ** 3), 2),
            "used_gb": round(psutil.disk_usage('/').used / (1024 ** 3), 2),
            "used_percent": psutil.disk_usage('/').percent
        },

        "battery": {
            "percent": battery.percent if battery else None,
            "plugged": battery.power_plugged if battery else None,
            "is_laptop": battery is not None
        },

        "screen": {
            "resolution": get_screen_resolution()
        },

        "network": {
            "ip": get_ip_address(),
            "mac": get_mac_address()
        }
    }
