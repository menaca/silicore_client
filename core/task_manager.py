import base64
import psutil
import pyautogui
from io import BytesIO
from datetime import datetime
from .system_info import get_system_info
from .utils import generate_code
from config.firebase_setup import collection

def handle_command(doc, client_id):
    data = doc.to_dict()
    command = data.get("command", "none")

    if command == "screenshot":
        img = pyautogui.screenshot()
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        encoded = base64.b64encode(buffered.getvalue()).decode()
        collection.document(client_id).update({
            "screenshot_base64": encoded,
            "screenshot_taken_at": datetime.now().isoformat()
        })

    elif command == "update_tasklist":
        update_tasklist(client_id)

    elif command == "kill_process":
        pid_list = data.get("target_pid_list", [])
        results = [kill_process(pid) for pid in pid_list]
        collection.document(client_id).update({
            "kill_results": results
        })

    elif command == "shutdown":
        print("[DEBUG] Shutdown command would be executed here.")

    collection.document(client_id).update({"command": "none"})

def update_tasklist(client_id):
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            processes.append({
                "pid": proc.info['pid'],
                "name": proc.info['name'],
                "cpu": proc.info['cpu_percent'],
                "memory": proc.info['memory_percent']
            })
        collection.document(client_id).update({
            "process_list": processes,
            "tasklist_updated_at": datetime.now().isoformat()
        })
        print(f"[{datetime.now()}] Tasklist uploaded.")
    except Exception as e:
        print(f"[{datetime.now()}] Tasklist error: {e}")

def kill_process(pid):
    try:
        p = psutil.Process(pid)
        p.terminate()
        print(f"[{datetime.now()}] Terminated process with PID {pid}")
        return f"Terminated process {pid}"
    except Exception as e:
        print(f"[{datetime.now()}] Error killing process {pid}: {e}")
        return str(e)