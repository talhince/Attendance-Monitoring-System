import customtkinter as ctk
from database import DatabaseManager
from views import AppWindow

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    db = DatabaseManager()
    app = AppWindow(db)
    app.mainloop()