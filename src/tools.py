import json, sys, os, hashlib, customtkinter as ctk, requests
from datetime import datetime
# from playsound import playsound



## GENERAL TOOLS
class GeneralTools():
    def __init__(self, api=None):
        self.api = api


    def save_json(self, data: dict, filename: str) -> None:
        with open(filename, 'w') as f:
            json.dump(data, f)


    def load_json(self, filename: str) -> dict:
        with open(filename, 'r') as f:
            return json.load(f)


    def load_txt(self, filename: str) -> str:
        with open(filename, 'r') as f:
            return f.read()


    def save_txt(self, data: str, filename: str) -> None:
        with open(filename, 'w') as f:
            f.write(data)


    def resource_path(self, relative_path: str) -> str:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base_path, relative_path)


    def write_log(self, message: str, type: str = "info") -> None:
        now = datetime.now()
        now_str = now.strftime("%H:%M:%S")
        if type == "info":
            file = self.resource_path("logs.txt")
        elif type == "error":
            file = self.resource_path("crash.txt")
        
        try:
            text = self.load_txt(file)
            text += f"[{now_str}] | {type.upper()}: {message}\n"
            self.save_txt(text, file)
        except FileNotFoundError:
            self.save_txt(f"[{now_str}] | {type.upper()}: {message}\n", file)

        print(f"[{now_str}] | {type.upper()}: {message}")


    def convert_game_time(self, iso_str: str):
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return round(dt.hour + dt.minute / 60 + dt.second / 3600, 2)


    def generate_job_id(self, job_data: dict) -> int:
        signature = f"{job_data['market']}_{job_data['source_city_id']}_{job_data['destination_city_id']}_{job_data['destination_company_id']}_{job_data['cargo_definition_id']}"
        hash_object = hashlib.md5(signature.encode())
        hash_int = int(hash_object.hexdigest(), 16)
        return hash_int % 1000000


    def get_switch_value(self, switch: ctk.CTkSwitch) -> bool:
        return True if switch.get() == 1 else False
    

    def get_latest_release(self) -> str:
        url = "https://api-kaelysvirtual.onrender.com/tracker/version"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['latestVersion']
        else:
            raise Exception(f"API error: {response.status_code}")