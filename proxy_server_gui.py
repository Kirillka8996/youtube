import tkinter as tk
from tkinter import messagebox
import threading
import subprocess
import sys

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Прокси-сервер")
        self.root.geometry("300x300")

        self.status_label = tk.Label(root, text="Статус: Остановлен", fg="red")
        self.status_label.pack(pady=20)

        self.start_button = tk.Button(root, text="Запустить", command=self.start_server)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Остановить", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

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

def run_gui():
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()