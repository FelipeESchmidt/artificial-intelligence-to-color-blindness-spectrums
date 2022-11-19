from multiprocessing import Pool
from transform import transform_line
from tkinter import filedialog
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import neurolab as nl
import numpy as np
import datetime

# Size for displaying Image
w = 400
h = 280
size = (w, h)


def start_app():
    global tk_window
    tk_window = Tk()
    tk_window.configure(background='white')
    tk_window.title("IA para daltônicos")

    tk_window.geometry(f'{1440}x{835}')
    tk_window.iconbitmap('./images/app.ico')
    tk_window.resizable(1, 1)

    render()


def apply_type(type_to):
    global type_selected
    type_selected = type_to
    apply_ai(nl.load('intelligence_' + type_to + '.net'))


def upload_im():
    try:
        global im, resized
        image_frame = tk.Frame(tk_window)
        image_frame.place(x=200, y=230)
        path = filedialog.askopenfilename()
        im = Image.open(path)
        im = im.convert('RGB')
        resized = im.resize(size, Image.ANTIALIAS)
        tk_image = ImageTk.PhotoImage(resized)
        display = tk.Label(image_frame)
        display.imgtk = tk_image
        display.configure(image=tk_image)
        display.grid()
        dn1 = tk.Label(tk_window, text='Imagem Original', width=30, height=1, fg="black", font=('times', 14, 'bold'))
        dn1.place(x=200, y=200)
    except:
        del im
        noti = tk.Label(tk_window, text='Problema ao carregar imagem', width=33, height=1, fg="white", bg="black",
                        font=('times', 15, ' bold '))
        noti.place(x=600, y=650)
        tk_window.after(5000, destroy_widget, noti)


def apply_ai(ai):
    try:
        global op

        img = np.array(np.asarray(im))

        with Pool(5) as p:
            result = (p.map_async(transform_line, [[line, ai] for line in img]))
            result.wait()
            new_img = np.array(result.get())

        op = Image.fromarray(np.uint8(new_img))

        resi = op.resize(size, Image.ANTIALIAS)
        tkimage3 = ImageTk.PhotoImage(resi)
        imageFrame3 = tk.Frame(tk_window)
        imageFrame3.place(x=950, y=230)
        dn3 = tk.Label(tk_window, text='Imagem Transformada com IA', width=30, height=1, fg="black",
                       font=('times', 14, ' bold '))
        dn3.place(x=950, y=200)
        display3 = tk.Label(imageFrame3)
        display3.imgtk = tkimage3
        display3.configure(image=tkimage3)
        display3.grid()
    except Exception as e:
        print(e)
        noti = tk.Label(tk_window, text='Carregue uma imagem primeiro', width=33, height=1, fg="white", bg="black",
                        font=('times', 15, ' bold '))
        noti.place(x=600, y=650)
        tk_window.after(5000, destroy_widget, noti)


def save_img():
    try:
        global noti, dna
        ts = datetime.datetime.now()
        current_date = ts.strftime("%Y-%m-%d_%H-%M-%S")
        filename = current_date + "_" + type_selected + ".jpg"
        op.save('./Captures/' + filename)

        dna = tk.Label(tk_window, text='Imagem salva em /Captures', width=33, height=1, fg="black", bg="spring green",
                       font=('times', 15, ' bold '))
        dna.place(x=600, y=650)
        tk_window.after(5000, destroy_widget, dna)
    except:
        noti = tk.Label(tk_window, text='Problema ao salvar as imagens', width=33, height=1, fg="white", bg="black",
                        font=('times', 15, ' bold '))
        noti.place(x=600, y=650)
        tk_window.after(5000, destroy_widget, noti)


def leave():
    from tkinter import messagebox
    if messagebox.askokcancel("Sair", "Você deseja sair?"):
        tk_window.destroy()


def destroy_widget(widget):
    widget.destroy()


def render():
    # BOTÃO DE UPLOAD
    up_image = PhotoImage(file="./images/upload.png")
    up = tk.Button(tk_window, image=up_image, bg="white", borderwidth=0, command=upload_im)
    up.place(x=20, y=50)
    upLab = tk.Label(tk_window, text="Carregar", bg="#e53935", fg="white", width=11, height=1,
                     font=('times', 16, 'italic bold '))
    upLab.place(x=20, y=160)
    # BOTÃO DE UPLOAD

    # BOTÃO DE SAVE
    save_image = PhotoImage(file="./images/save.png")
    save = tk.Button(tk_window, borderwidth=0, bg='white', image=save_image, command=save_img)
    save.place(x=20, y=290)
    saveLab = tk.Label(tk_window, text="Salvar", bg="#e53935", fg="white", width=11, height=1,
                       font=('times', 16, 'italic bold '))
    saveLab.place(x=20, y=400)
    # BOTÃO DE SAVE

    # BOTÃO DE QUIT
    quit_image = PhotoImage(file="./images/quit.png")
    q = tk.Button(tk_window, borderwidth=0, bg='white', image=quit_image, command=leave)
    q.place(x=20, y=530)
    quitLab = tk.Label(tk_window, text="Sair", bg="#e53935", fg="white", width=11, height=1,
                       font=('times', 16, 'italic bold '))
    quitLab.place(x=20, y=640)
    # BOTÃO DE QUIT

    # BOTÃO DE PROTANOPIA
    med = tk.Button(tk_window, borderwidth=0, bg='#1e88e5', fg="white", width=11, text='Protanopia',
                    font=('times', 16, 'italic bold '), command=lambda: apply_type('prot'))
    med.place(x=700, y=280)
    # BOTÃO DE PROTANOPIA

    # BOTÃO DE DEUTERANOPIA
    med = tk.Button(tk_window, borderwidth=0, bg='#1e88e5', fg="white", width=11, text='Deuteranopia',
                    font=('times', 16, 'italic bold '), command=lambda: apply_type('deut'))
    med.place(x=700, y=360)
    # BOTÃO DE DEUTERANOPIA

    # BOTÃO DE TRITANOPIA
    med = tk.Button(tk_window, borderwidth=0, bg='#1e88e5', fg="white", width=11, text='Tritanopia',
                    font=('times', 16, 'italic bold '), command=lambda: apply_type('trit'))
    med.place(x=700, y=440)
    # BOTÃO DE TRITANOPIA

    names = tk.Label(tk_window, text="© Developed by Felipe E. Schmidt ©", bg="#616161", fg="white", width=67,
                     height=2, font=('times', 30, 'italic bold '))
    names.place(x=00, y=740)

    # tk_window.protocol("WM_DELETE_WINDOW", leave)
    tk_window.mainloop()


if __name__ == '__main__':
    start_app()
