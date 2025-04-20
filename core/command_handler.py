import base64
import pyautogui
from io import BytesIO
from datetime import datetime
from .task_manager import update_tasklist, kill_process
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
        
        print(f"[{datetime.now()}] Screenshot uploaded as base64.")


    elif command == "update_tasklist":
        update_tasklist(client_id)

    elif command == "kill_process":
        pid_list = data.get("target_pid_list", [])
        results = [kill_process(pid) for pid in pid_list]
        collection.document(client_id).update({
            "kill_results": results
        })

    elif command == "shutdown":
        try:
            #os.system("shutdown /s /t 5")
            print(f"[{datetime.now()}] Shutdown command executed.")
        except Exception as e:
            print(f"[{datetime.now()}] Shutdown error: {e}")

    collection.document(client_id).update({"command": "none"})
