import tkinter as tk
from tkinter import filedialog, messagebox, Scale, Label, Button
from PIL import Image, ImageTk, ImageOps
from datetime import datetime
import json
import os


class ImageComparatorApp:
    def __init__(self, root, on_close):
        self.root = root
        self.root.title("Diagnóstico Probable de Melanoma")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", on_close)

        self.set_background('imgD/Analisis2.png')

        self.upload_button = Button(root, text="Capturar Imagen", command=self.upload_image, bg="#F3D64C",
                                    font=("Arial", 12, "bold"))
        self.upload_button.place(x=230, y=160, width=180, height=40)

        self.image_frame = tk.Frame(root, width=600, height=400)
        self.image_frame.place(x=52, y=240, width=535, height=320)
        self.image_label = Label(self.image_frame, bg="black")
        self.image_label.pack(expand=True, fill='both')

        self.info_frame = tk.Frame(root, width=400, height=600, bg="yellow")
        self.info_frame.place(x=634, y=180, width=250, height=400)

        self.probability_scale = Scale(self.info_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                       label="Probabilidad de Melanoma", bg="yellow")
        self.probability_scale.pack(pady=20)

        self.diagnosis_label = Label(self.info_frame, text="Probabilidad: Baja", font=("Arial", 16), bg="yellow")
        self.diagnosis_label.pack(pady=20)

        self.probability_label = Label(self.info_frame, text="0%", font=("Arial", 24), bg="yellow")
        self.probability_label.pack(pady=20)

        self.datetime_label = Label(self.info_frame,
                                    text=f"Hora: {datetime.now().strftime('%H:%M:%S')}\nFecha: {datetime.now().strftime('%d/%m/%Y')}",
                                    font=("Arial", 16), bg="yellow")
        self.datetime_label.pack(pady=20)

        if not os.path.exists('img'):
            os.makedirs('img')
        self.image_data_path = os.path.join('img', 'image_data.json')
        self.image_data = self.load_image_data()

    def set_background(self, image_path):
        image = Image.open(image_path)
        image = image.resize((1200, 700), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)

        canvas = tk.Canvas(self.root, width=1200, height=700)
        canvas.pack(fill='both', expand=True)
        canvas.create_image(0, 0, image=self.background_image, anchor='nw')
        canvas.lower('all')

    def load_image_data(self):
        if os.path.exists(self.image_data_path):
            with open(self.image_data_path, 'r') as f:
                return json.load(f)
        return {}

    def save_image_data(self):
        with open(self.image_data_path, 'w') as f:
            json.dump(self.image_data, f)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.display_image(file_path, grayscale=True)  # Cambiar a escala de grises
            self.update_diagnosis(file_path)

    def display_image(self, file_path, grayscale=False):
        image = Image.open(file_path)

        if grayscale:
            image = ImageOps.grayscale(image)

        img_width, img_height = image.size
        max_width, max_height = 535, 320

        if img_width > max_width or img_height > max_height:
            ratio = min(max_width / img_width, max_height / img_height)
            new_size = (int(img_width * ratio), int(img_height * ratio))
            image = image.resize(new_size, Image.LANCZOS)

        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo, width=max_width, height=max_height, anchor='center')
        self.image_label.image = photo

    def update_diagnosis(self, file_path):
        if file_path in self.image_data:
            probability = self.image_data[file_path]['probability']
        else:
            import random
            probability = random.randint(0, 100)
            self.image_data[file_path] = {'probability': probability}
            self.save_image_data()

        self.probability_scale.set(probability)
        self.probability_label.config(text=f"{probability}%")
        self.diagnosis_label.config(text=self.get_probability_diagnosis(probability))
        self.datetime_label.config(
            text=f"Hora: {datetime.now().strftime('%H:%M:%S')}\nFecha: {datetime.now().strftime('%d/%m/%Y')}")

    def get_probability_diagnosis(self, probability):
        if probability < 35:
            return "Probabilidad: Baja"
        elif probability < 70:
            return "Probabilidad: Media"
        else:
            return "Probabilidad: Alta"


def on_close():
    root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageComparatorApp(root, on_close)
    root.mainloop()
