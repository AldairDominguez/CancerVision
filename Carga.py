import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
import os
import queue

root = tk.Tk()
root.title("Ventana de Carga")
window_width = 1200
window_height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_x = int((screen_width / 2) - (window_width / 2))
position_y = int((screen_height / 2) - (window_height / 2))

root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

background_image = Image.open("imgD/carga.png")
background_image = background_image.resize((1200, 700), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=1200, height=700)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

progress = ttk.Progressbar(canvas, orient="horizontal", mode="determinate", length=1160)
progress.place(x=20, y=660)

q = queue.Queue()

def update_progress():
    try:
        value = q.get_nowait()
    except queue.Empty:
        root.after(100, update_progress)
        return

    progress["value"] = value
    if value < 100:
        root.after(100, update_progress)
    else:
        root.destroy()
        os.system('python Menu.py')

def load_in_background():
    for i in range(101):
        time.sleep(0.15)
        q.put(i)

root.after(90, update_progress)

thread = threading.Thread(target=load_in_background)
thread.start()
root.mainloop()
