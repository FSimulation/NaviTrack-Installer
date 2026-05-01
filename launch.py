import customtkinter as ctk
import wget, shutil, os, subprocess, threading
from PIL import Image
from src.tools import GeneralTools


tools = GeneralTools()


class InstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NaviTrack Client - Installer")
        self.geometry("600x350")
        self.resizable(False, False)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.custom_font = ctk.CTkFont(family="Poppins", size=18, weight="bold")
        self.configure(fg_color="#0e1a27")
        ctk.set_appearance_mode("Dark")
        self.resizable(False, False)

        # Paramètres de l'app
        self.ZIP_URL = "https://github.com/FSimulation/NaviTrack/releases/download/public-latest/NaviTrack.zip"
        self.APP_DIR = "NaviTrack"
        self.APP_EXE = os.path.join(self.APP_DIR, "NaviTrack.exe")
        self.TMP_ZIP = "NaviTrack_tmp.zip"

        self.setup_ui()


    def setup_ui(self):
        # MAIN LOGO 
        banner = Image.open(tools.resource_path("src/static/launcher_logo.png"))
        # banner = original.resize((1200, 180))  # largeur fenêtre, hauteur bannière
        banner_img = ctk.CTkImage(light_image=banner, dark_image=banner, size=(630, 190))
        banner_label = ctk.CTkLabel(self, image=banner_img, text="")
        banner_label.pack(pady=(5, 5))

        # VERSION LABEL
        self.version_label = ctk.CTkLabel(self, text="", font=("Arial", 16), text_color="#8fa7be")
        self.version_label.pack()

        # STATUS LABEL
        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 16), text_color="#8fa7be")
        self.status_label.pack(pady=5)
        self.display_latest_version()

        # INSTALL BUTTON
        self.install_button = ctk.CTkButton(self, text="Install / Update", font=self.custom_font, command=self.on_update_click)
        self.install_button.pack()

        # STATUS LABEL
        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 16), text_color="#8fa7be")
        self.status_label.pack(pady=5)


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

    
    def display_latest_version(self):
        try:
            # Récupérer les infos de la dernière release depuis l'API GitHub
            latest_release = tools.get_latest_release()
            self.version_label.configure(text=f"Latest version: {latest_release}")
        except Exception as e:
            self.version_label.configure(text=f"⚠️ Error fetching version: {e}")



if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()
