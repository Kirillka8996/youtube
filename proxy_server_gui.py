import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kirillka DPI")
        self.root.geometry("300x300")

        # Тема по умолчанию (светлая)
        self.theme = "dark"  # Изменено на "dark" для темно-серой темы

        # Создание виджетов
        self.status_label = tk.Label(root, text="Статус: Остановлен", fg="red")
        self.status_label.pack(pady=20)

        # Указываем одинаковую ширину для всех кнопок
        button_width = 15

        self.start_button = tk.Button(root, text="Запустить", command=self.start_server, width=button_width)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Остановить", command=self.stop_server, state=tk.DISABLED, width=button_width)
        self.stop_button.pack(pady=10)

        self.theme_button = tk.Button(root, text="Сменить тему", command=self.toggle_theme, width=button_width)
        self.theme_button.pack(pady=10)

        # Применение темы после создания всех виджетов
        self.apply_theme()

        self.server_process = None

    def start_server(self):
        if self.server_process is not None:
            messagebox.showwarning("Внимание", "Сервер уже запущен!")
            return

        self.server_process = subprocess.Popen([sys.executable, "proxy_server.py"])
        self.status_label.config(text="Статус: Запущен", fg="green")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_server(self):
        if self.server_process is None:
            messagebox.showwarning("Внимание", "Сервер не запущен!")
            return

        self.server_process.terminate()
        self.server_process = None
        self.status_label.config(text="Статус: Остановлен", fg="red")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def toggle_theme(self):
        """Переключение между светлой и темной темами."""
        if self.theme == "light":
            self.theme = "dark"
        else:
            self.theme = "light"
        self.apply_theme()

    def apply_theme(self):
        """Применение выбранной темы."""
        if self.theme == "light":
            self.root.configure(bg="white")
            self.status_label.configure(bg="white", fg="black")
            self.start_button.configure(bg="white", fg="black")
            self.stop_button.configure(bg="white", fg="black")
            self.theme_button.configure(bg="white", fg="black")
        else:
            # Темно-серая тема
            dark_gray = "gray20"  # Стандартный темно-серый цвет в Tkinter
            self.root.configure(bg=dark_gray)
            self.status_label.configure(bg=dark_gray, fg="white")
            self.start_button.configure(bg=dark_gray, fg="white")
            self.stop_button.configure(bg=dark_gray, fg="white")
            self.theme_button.configure(bg=dark_gray, fg="white")

def run_gui():
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()