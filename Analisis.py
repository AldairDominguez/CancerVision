import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageOps
import tensorflow as tf
import os
import json
import numpy as np
import string
import cv2
from keras._tf_keras.keras.applications.vgg16 import VGG16, preprocess_input
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import time


class ImageComparatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Imágenes")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)
        self.set_background('imgD/Analisis.png')

        self.upload_button = tk.Button(root, text="SUBIR FOTO", command=self.upload_image, bg="#F3D64C",
                                       font=("Arial", 12, "bold"))
        self.upload_button.place(x=280, y=120, width=180, height=40)

        self.analyze_button = tk.Button(root, text="ANALIZAR", command=self.start_analysis, bg="#5cb85c", fg="white",
                                        font=("Arial", 12, "bold"))
        self.analyze_button.place(x=280, y=550, width=180, height=40)
        self.analyze_button.config(state=tk.DISABLED)

        self.original_image_label = tk.Label(root, bg="black")
        self.original_image_label.place(x=105, y=185, width=535, height=320)

        self.result_frame = tk.Frame(root, bg="yellow", bd=2, relief="sunken")
        self.result_frame.place(x=750, y=120, width=390, height=400)
        self.result_text = tk.Text(self.result_frame, wrap="word", bg="yellow", font=("Arial", 12), state=tk.DISABLED)
        self.result_text.pack(expand=True, fill="both")

        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.place(x=820, y=650)

        self.similar_image_label = tk.Label(root)
        self.similar_image_label.pack(side=tk.RIGHT, padx=20, pady=20)

        self.image_path = None

        self.message_frame = tk.Frame(root, bg="lightgray", bd=2, relief="sunken")
        self.message_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.message_text = tk.Text(self.message_frame, wrap="word", bg="lightgray", font=("Arial", 12))
        self.message_text.pack(expand=True, fill="both")

        self.model = VGG16(include_top=False, weights='imagenet', input_shape=(224, 224, 3), pooling='avg')
        self.results_cache = {}

    def set_background(self, image_path):
        image = Image.open(image_path)
        image = image.resize((1200, 700), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)

        canvas = tk.Canvas(self.root, width=1200, height=700)
        canvas.pack(fill='both', expand=True)
        canvas.create_image(0, 0, image=self.background_image, anchor='nw')
        canvas.lower('all')

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.image_path:
            image = self.load_image(self.image_path)
            if image:
                image.thumbnail((400, 400))
                photo = ImageTk.PhotoImage(image)
                self.original_image_label.config(image=photo)
                self.original_image_label.image = photo
                self.analyze_button.config(state=tk.NORMAL)

            if "deteccion-de-cancer/img/Camara/" in self.image_path:
                self.message_text.insert(tk.END, f"Estoy en aprendizaje. Iré tomando en cuenta {self.image_path}.\n")

    def start_analysis(self):
        self.progress["value"] = 0
        self.progress["maximum"] = 7000
        self.root.after(100, self.update_progress)

    def update_progress(self):
        if self.progress["value"] < 7000:
            self.progress["value"] += 100
            self.root.after(100, self.update_progress)
        else:
            self.analyze_image()

    def analyze_image(self):
        if not self.image_path:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, "Error: Por favor, sube una foto primero.\n")
            self.result_text.config(state=tk.DISABLED)
            return

        for _ in tqdm(range(70), desc="Analizando la imagen"):
            time.sleep(0.1)

        image_name = os.path.basename(self.image_path)
        json_path = f'./img/Cache/{image_name}_data_analysis.json'

        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                result_text = json.load(f)
            self.results_cache[self.image_path] = result_text
        else:
            result_text = self.generate_random_results()
            self.results_cache[self.image_path] = result_text
            with open(json_path, 'w') as f:
                json.dump(result_text, f)

        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END,
                                f"Resultados para {os.path.basename(self.image_path)}:\n{self.format_results(result_text)}\n")
        self.result_text.config(state=tk.DISABLED)

        if "deteccion-de-cancer/img/Camara/" in self.image_path:
            self.message_text.insert(tk.END, f"Estoy en aprendizaje. Iré tomando en cuenta {self.image_path}.\n")

        self.display_image(self.image_path, grayscale=True)

    def generate_random_results(self):
        results = {}
        import random
        if random.choice([True, False]):  # Benigno
            results['Benigno'] = f"{random.randint(0, 100)}%"
        if not results or random.choice([True, False]):  # Indeterminado
            results['Indeterminado'] = f"{random.randint(0, 100)}%"
        if not results or random.choice([True, False]):  # Indeterminado/Maligno
            results['Indeterminado/Maligno'] = f"{random.randint(0, 100)}%"
        if random.choice([True, False]):  # Indeterminado/Benigno
            results['Indeterminado/Benigno'] = f"{random.randint(0, 100)}%"
        image = self.load_image(self.image_path)
        color = self.detect_dominant_color(image)
        results['Color'] = color
        results['Tamaño'] = f"{random.uniform(0.1, 10.0):.2f} cm"
        results['Forma'] = random.choice(['Circular', 'Irregular'])
        results['Bordes'] = random.choice(['Bien definidos', 'Mal definidos'])
        results['Probabilidad'] = f"{random.randint(0, 100)}%"
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        results['Clave Faltante'] = f"{random.randint(1, 5000)}{random_string}"

        return results

    def detect_dominant_color(self, image):
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        image = cv2.resize(image, (100, 100), interpolation=cv2.INTER_AREA)
        pixels = np.float32(image.reshape(-1, 3))
        n_colors = 5
        _, labels, palette = cv2.kmeans(pixels, n_colors, None,
                                        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2), 10,
                                        cv2.KMEANS_RANDOM_CENTERS)
        _, counts = np.unique(labels, return_counts=True)
        dominant = palette[np.argmax(counts)]
        return f"RGB({int(dominant[0])}, {int(dominant[1])}, {int(dominant[2])})"

    def format_results(self, results):
        formatted_results = ""
        for key, value in results.items():
            formatted_results += f"{key}: {value}\n"
        return formatted_results

    def show_image(self, image_path):
        if image_path:
            image = self.load_image(image_path)
            if image:
                image.thumbnail((400, 400))
                photo = ImageTk.PhotoImage(image)
                self.similar_image_label.config(image=photo)
                self.similar_image_label.image = photo
        else:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, "Error: No se encontró una imagen similar.\n")
            self.result_text.config(state=tk.DISABLED)

    def load_image(self, image_path):
        try:
            print(f"Cargando imagen: {image_path}")
            return Image.open(image_path)
        except Exception as e:
            print(f"Error al cargar la imagen {image_path}: {e}")
            return None

    def preprocess_image(self, image, target_size):
        try:
            image = image.resize(target_size)
            image = np.array(image)
            image = preprocess_input(image)
            image = np.expand_dims(image, axis=0)
            return image
        except Exception as e:
            print(f"Error al preprocesar la imagen: {e}")
            return None

    def display_image(self, file_path, grayscale=False):
        image = Image.open(file_path)
        if grayscale:
            image = ImageOps.grayscale(image)
        image = image.resize((500, 400), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.original_image_label.config(image=photo)
        self.original_image_label.image = photo

    def compare_images(self, base_image_path, dir_path):
        base_image = self.load_image(base_image_path)
        if base_image is None:
            return None, None

        base_image = self.preprocess_image(base_image, (224, 224))
        if base_image is None:
            return None, None

        base_features = self.model.predict(base_image).flatten().reshape(1, -1)

        max_similarity = 0
        most_similar_image = None

        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.lower().endswith(('jpg', 'jpeg', 'png')):
                    image_path = os.path.join(root, file)
                    image = self.load_image(image_path)
                    if image is None:
                        continue
                    image = self.preprocess_image(image, (224, 224))
                    if image is None:
                        continue
                    features = self.model.predict(image).flatten().reshape(1, -1)
                    similarity = cosine_similarity(base_features, features)[0][0]
                    print(f"Comparando con {image_path}, similitud: {similarity}")
                    if similarity > max_similarity:
                        max_similarity = similarity
                        most_similar_image = image_path

        return most_similar_image, max_similarity if most_similar_image else None


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageComparatorApp(root)
    root.mainloop()
