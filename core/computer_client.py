import json
import time
from datetime import datetime
from config.firebase_setup import collection, JSON_PATH
from .utils import generate_code
from .system_info import get_system_info
from .command_handler import handle_command
import ui.connection_ui as ui
from firebase_admin import credentials, firestore, delete_app
import firebase_admin

class ComputerClient:
    def __init__(self):
        self.key_data = self._load_config()
        self.client_id = self._get_or_create_client_id()

    def _load_config(self):
        with open(JSON_PATH, "r") as f:
            return json.load(f)

    def _get_or_create_client_id(self):
        if self.key_data.get("custom_client_id"):
            return self.key_data["custom_client_id"]

        temp_cred = credentials.Certificate(self.key_data)
        temp_app = firebase_admin.initialize_app(temp_cred, name="temp")
        db = firestore.client(temp_app)

        doc_ref = collection.document()
        code = generate_code()

        doc_ref.set({
            "computer_name": get_system_info()["computer_name"],
            "initialized_at": datetime.now().isoformat(),
            "status": "initialized",
            "connectedStatus": "waiting",
            "connection_code": code
        })

        client_id = doc_ref.id
        self.key_data["custom_client_id"] = client_id

        with open(JSON_PATH, "w") as f:
            json.dump(self.key_data, f, indent=2)

        delete_app(temp_app)

        print(f"[{datetime.now()}] Client created.")

        return client_id

    def run(self):
        print(f"[{datetime.now()}] Client started...")
        while True:
            self._check_connection_status()
            self._send_info()
            self._check_for_command()
            time.sleep(10)

    def _send_info(self):
        try:
            collection.document(self.client_id).update(get_system_info())
            print(f"[{datetime.now()}] Info updated.")
        except Exception as e:
            print(f"Error sending info: {e}")

    def _check_for_command(self):
        try:
            doc = collection.document(self.client_id).get()
            if doc.exists:
                handle_command(doc, self.client_id)
        except Exception as e:
            print(f"Error checking command: {e}")

    def _check_connection_status(self):
        try:
            doc = collection.document(self.client_id).get()
            if doc.exists:
                data = doc.to_dict()
                status = data.get("connectedStatus", "waiting")
                code = data.get("connection_code", "")

                if status in ["waiting", "disconnected"]:
                    print(f"[{datetime.now()}] Status: {status} - Showing UI")
                    if not ui.is_window_open():
                        ui.show_connection_window(code)
                else:
                    print(f"[{datetime.now()}] Connected to phone")
                    if ui.is_window_open():
                        ui.close_connection_window()
        except Exception as e:
            print(f"Connection check failed: {e}")
