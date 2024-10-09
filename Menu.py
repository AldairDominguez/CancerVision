import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import importlib.util
import os
import subprocess

import Keras

analisis_path = 'analisis.py'
spec = importlib.util.spec_from_file_location("ImageComparatorApp", analisis_path)
analisis_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analisis_module)

scanner_script_path = 'esc.py'

def open_analysis_window(root):
    def on_close():
        root.deiconify()
        analysis_root.destroy()

    root.withdraw()
    analysis_root = tk.Toplevel()
    app = analisis_module.ImageComparatorApp(analysis_root)
    analysis_root.protocol("WM_DELETE_WINDOW", on_close)
    analysis_root.mainloop()

def open_diagnosis_window(root):
    def on_close():
        root.deiconify()
        diag_root.destroy()

    root.withdraw()
    diag_root = tk.Toplevel()
    app = Keras.ImageComparatorApp(diag_root, on_close)
    diag_root.mainloop()

def open_doctor_consultation(root):
    def on_close():
        root.deiconify()
        doctor_root.destroy()

    root.withdraw()
    bot2_path = 'bot2.py'
    spec = importlib.util.spec_from_file_location("DoctorBotApp", bot2_path)
    bot2_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bot2_module)

    doctor_root = tk.Toplevel()
    app = bot2_module.DoctorBotApp(doctor_root, on_close)
    doctor_root.mainloop()

def open_scanner_window(root):
    root.withdraw()
    process = subprocess.Popen(['python', scanner_script_path])
    process.wait()
    root.deiconify()

class CustomButton(tk.Canvas):
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.default_color = '#f0c929'
        self.hover_color = '#e0b823'
        self.configure(height=50, width=300)
        self.create_rectangle(0, 0, 300, 50, outline='#f0f0f0', fill=self.default_color, width=2, tags="rect")
        self.create_text(150, 25, text=text, fill='black', font=('Arial', 12, 'bold'), tags="text")
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_click(self, event):
        self.command()

    def on_enter(self, event):
        self.itemconfig("rect", fill=self.hover_color)

    def on_leave(self, event):
        self.itemconfig("rect", fill=self.default_color)

class MainMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)

        self.bg_image = Image.open("imgD/menu.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((1200, 700), Image.LANCZOS))

        self.canvas = tk.Canvas(root, width=1200, height=700)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.analyze_cancer_button = CustomButton(self.canvas, text="Análisis de Cáncer",
                                                  command=lambda: open_analysis_window(root))
        self.canvas.create_window(800, 200, window=self.analyze_cancer_button)

        self.diagnosis_melanoma_button = CustomButton(self.canvas, text="Diagnóstico de Melanoma",
                                                      command=lambda: open_diagnosis_window(root))
        self.canvas.create_window(800, 280, window=self.diagnosis_melanoma_button)

        self.consult_doctor_button = CustomButton(self.canvas, text="Consulta Doctor (Bot)",
                                                  command=lambda: open_doctor_consultation(root))
        self.canvas.create_window(800, 360, window=self.consult_doctor_button)

        self.scanner_button = CustomButton(self.canvas, text="Escáner", command=lambda: open_scanner_window(root))
        self.canvas.create_window(800, 440, window=self.scanner_button)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenuApp(root)
    root.mainloop()
