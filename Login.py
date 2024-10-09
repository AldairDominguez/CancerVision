import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk
import os

root = tk.Tk()
root.title('Login')
root.resizable(False, False)
window_width = 925
window_height = 500

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_x = int((screen_width / 2) - (window_width / 2))
position_y = int((screen_height / 2) - (window_height / 2))

root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

background_image = Image.open("img/login/fondo-login-p.png")
background_image = background_image.resize((window_width, window_height), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=1200, height=700)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

frame = tk.Frame(root, width=350, height=290, bg="white", border=2)
frame.place(x=550, y=150)

def on_resize(event):
    canvas.config(width=event.width, height=event.height)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")

canvas.bind('<Configure>', on_resize)

heading = tk.Label(frame, text="LOGIN", fg="black", bg="white", font=("Microsoft YaHei UI Light", 23, 'bold'))
heading.place(x=110, y=5)

def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Nombre de Usuario')

def signin():
    username = user.get()
    password = code.get()

    if username == 'admin' and password == '1234':
        root.destroy()
        os.system('python Carga.py')

    elif username != 'admin' and password != '1234':
        messagebox.showerror("Invalido", "Usuario y contraseña Invalidos")
    elif password != "1234":
        messagebox.showerror("Invalido", "Contraseña Invalida")
    elif username != 'admin':
        messagebox.showerror("Invalido", "Usuario Invalido")

user = tk.Entry(frame, width=32, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
user.place(x=30, y=80)
user.insert(0, 'Nombre de Usuario')

user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

tk.Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

def on_enter(e):
    code.delete(0, 'end')
    code.config(show='*')

def on_leave(e):
    name = code.get()
    if name == '':
        code.config(show='')
        code.insert(0, 'Contraseña')

code = tk.Entry(frame, width=32, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11), show='*')
code.place(x=30, y=150)
code.insert(0, 'Contraseña')
code.config(show='')

code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

tk.Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

button_font = tkfont.Font(family="Poppins", size=13, weight="bold")
tk.Button(frame, width=25, pady=4, text='INICIAR SESIÓN', bg='#c1ff72', fg='black',
          font=button_font, border=5, command=signin).place(x=35, y=204)

root.mainloop()
