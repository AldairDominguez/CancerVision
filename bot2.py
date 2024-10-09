import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import threading

class DoctorBotApp:
    def __init__(self, root, on_close_callback):
        self.root = root
        self.root.title("Chatbot Doctor")
        self.on_close_callback = on_close_callback
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.geometry("1200x700")
        self.root.resizable(False, False)  # Disable maximizing

        # Load and set background image
        self.bg_image = Image.open('imgD/bot2.png')
        self.bg_image = self.bg_image.resize((1200, 700), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.query_entry = tk.Entry(root, width=80)
        self.query_entry.place(x=390, y=50)

        self.send_button = tk.Button(root, text="Enviar", command=self.send_query, bg="#C1FF72",
                                     activebackground="#C1FF72", width=30, height=5)
        self.send_button.place(x=900, y=60)

        self.response_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=88, height=20)
        self.response_text.place(x=35, y=190)

        self.progress_bar = ttk.Progressbar(root, mode='indeterminate')
        self.progress_bar.place(x=50, y=650, width=1100)

        self.response_text.tag_config('highlight', background='yellow')

    def send_query(self):
        query = self.query_entry.get()
        if not query.strip():  # Check if the query is empty
            self.response_text.insert(tk.END, "Por favor, ingrese una consulta.\n", 'highlight')
            return

        self.query_entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        threading.Thread(target=self.interact_with_bot, args=(query,)).start()

    def typewriter_effect(self, widget, text, tag_name):
        widget.config(state=tk.NORMAL)
        widget.delete(1.0, tk.END)
        for char in text:
            widget.insert(tk.END, char, tag_name)
            widget.update()
            time.sleep(0.05)
        widget.config(state=tk.DISABLED)

    def show_loading(self):
        self.progress_bar.start()

    def hide_loading(self):
        self.progress_bar.stop()

    def interact_with_bot(self, query):
        self.show_loading()

        driver_path = 'C:/chromedriver-win64/chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        service = webdriver.chrome.service.Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get('http://127.0.0.1:8080/')
            time.sleep(3)

            model_select = driver.find_element(By.ID, 'model')
            for option in model_select.find_elements(By.TAG_NAME, 'option'):
                if option.text == 'gpt-4o':
                    option.click()
                    break

            time.sleep(1)

            input_box = driver.find_element(By.XPATH, '//textarea[@placeholder="Ask a question"]')
            input_box.send_keys(query)
            input_box.send_keys(Keys.RETURN)

            time.sleep(15)

            messages = driver.find_elements(By.CLASS_NAME, 'message')
            if len(messages) > 0:
                last_message = messages[-1].text
                if 'Liaobots with gpt-4o' in last_message:
                    last_message = last_message.replace('Liaobots with gpt-4o', '').strip()
                if '(' in last_message and ')' in last_message:
                    last_message = last_message.split('(', 1)[0].strip()
            else:
                last_message = "No response found."

            self.response_text.insert(tk.END, f"User: {query}\n", 'highlight')
            self.response_text.insert(tk.END, "Bot: ", 'highlight')
            self.typewriter_effect(self.response_text, last_message, 'highlight')

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            self.response_text.insert(tk.END, f"User: {query}\n", 'highlight')
            self.response_text.insert(tk.END, "Bot: Error while fetching the response.\n", 'highlight')

        finally:
            driver.quit()
            self.hide_loading()
            self.query_entry.config(state=tk.NORMAL)
            self.send_button.config(state=tk.NORMAL)

    def on_close(self):
        self.on_close_callback()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DoctorBotApp(root, lambda: None)
    root.mainloop()
