import customtkinter as ctk
import requests, zipfile, io, shutil, os, subprocess
import threading


# URL du zip contenant le dossier OneDir
ZIP_URL = "https://github.com/FSimulation/myKaelys-Client-Releases/raw/public/myKaelys.zip"
APP_DIR = "myKaelys"
APP_EXE = os.path.join(APP_DIR, "MonApp.exe")


# Fonction de mise à jour
def update_app():
    status_label.configure(text="🔎 Downloading...")
    try:
        r = requests.get(ZIP_URL, stream=True)
        if r.status_code == 200:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            if os.path.exists(APP_DIR):
                shutil.rmtree(APP_DIR)
            z.extractall(APP_DIR)
            status_label.configure(text="✅ Installation complete! You can now close this window.")
        else:
            status_label.configure(text="⚠️ Unable to download the application.")
    except Exception as e:
        status_label.configure(text=f"⚠️ Error : {e}")


# Fonction pour lancer la mise à jour dans un thread
def on_update_click():
    threading.Thread(target=update_app).start()


# Interface
class InstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MyKaelys Client - Installer")
        self.geometry("400x200")
        self.resizable(False, False)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.custom_font = ctk.CTkFont(family="Poppins", size=18, weight="bold")
    

    def setup_ui(self):
        self.label = ctk.CTkLabel(self, text="myKaelys Client - Installer", font=self.custom_font)
        self.label.pack(pady=20)

        self.info_label = ctk.CTkLabel(self, text="Click the button below to install/update the application.")

        self.update_button = ctk.CTkButton(self, text="Start", command=on_update_click)
        self.update_button.pack(pady=10)

        global status_label
        status_label = ctk.CTkLabel(self, text="")
        status_label.pack(pady=10)


if __name__ == "__main__":
    app = InstallerApp()
    app.setup_ui()
    app.mainloop()



