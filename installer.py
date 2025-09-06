import customtkinter as ctk
import wget
import shutil, os, subprocess, threading



class InstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MyKaelys Client - Installer")
        self.geometry("400x220")
        self.resizable(False, False)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.custom_font = ctk.CTkFont(family="Poppins", size=18, weight="bold")

        # Paramètres de l'app
        self.ZIP_URL = "https://github.com/FSimulation/Kaelys-Tracker/releases/download/public-latest/myKaelys.zip"
        self.APP_DIR = "myKaelys"
        self.APP_EXE = os.path.join(self.APP_DIR, "myKaelys.exe")
        self.TMP_ZIP = "myKaelys_tmp.zip"

        self.setup_ui()


    def setup_ui(self):
        self.label = ctk.CTkLabel(self, text="myKaelys Client - Installer", font=self.custom_font)
        self.label.pack(pady=20)

        self.info_label = ctk.CTkLabel(self, text="Click the button below to install/update the application.")
        self.info_label.pack(pady=5)

        self.update_button = ctk.CTkButton(self, text="Start", command=self.on_update_click)
        self.update_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)


    # Lancer la mise à jour dans un thread
    def on_update_click(self):
        threading.Thread(target=self.update_app).start()


    # Fonction de mise à jour
    def update_app(self):
        self.status_label.configure(text="⬇️ Downloading latest version...")
        try:
            # Télécharger le zip avec wget
            wget.download(self.ZIP_URL, self.TMP_ZIP)

            # Supprimer l'ancien dossier si il existe
            if os.path.exists(self.APP_DIR):
                shutil.rmtree(self.APP_DIR)

            # Extraire le zip avec shutil.unpack_archive (plus tolérant)
            shutil.unpack_archive(self.TMP_ZIP, self.APP_DIR)

            # Supprimer le zip temporaire
            os.remove(self.TMP_ZIP)

            self.status_label.configure(text="✅ Installation complete!")

            # Relancer l'app
            subprocess.Popen([self.APP_EXE])

        except Exception as e:
            self.status_label.configure(text=f"⚠️ Error: {e}")



if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()
