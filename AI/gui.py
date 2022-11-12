from tkinter import filedialog
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import neurolab as nl
import numpy as np
import datetime

tk_window = Tk()
tk_window.configure(background='white')
tk_window.title("IA para daltônicos")
width = tk_window.winfo_screenwidth()
height = tk_window.winfo_screenheight()
tk_window.geometry(f'{width}x{height}')
tk_window.iconbitmap('./images/app.ico')
tk_window.resizable(0, 0)

# Size for displaying Image
w = 400
h = 280
size = (w, h)


def upload_im():
    try:
        global im, resized
        image_frame = tk.Frame(tk_window)
        image_frame.place(x=200, y=230)
        path = filedialog.askopenfilename()
        im = Image.open(path)
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
        noti.place(x=240, y=500)
        tk_window.after(5000, destroy_widget, noti)


def apply_ai(ai):
    try:
        global op

        img = np.asarray(im)
        new_img = np.array(im)

        for i in range(len(img)):
            i_arrays = img[i][:, :3]
            for j in range(len(i_arrays)):
                transformed = ai.sim([i_arrays[j] / 255])[0] * 255
                if img.shape[2] == 3:
                    new_img[i][j] = transformed
                else:
                    new_img[i][j] = np.append(transformed, [255])


        op = Image.fromarray(new_img)
        resi = op.resize(size, Image.ANTIALIAS)
        tkimage3 = ImageTk.PhotoImage(resi)
        imageFrame3 = tk.Frame(tk_window)
        imageFrame3.place(x=width - w - 200, y=230)
        dn3 = tk.Label(tk_window, text='Imagem Filtrada (Laplaciano)', width=30, height=1, fg="black",
                       font=('times', 14, ' bold '))
        dn3.place(x=width - w - 200, y=200)
        display3 = tk.Label(imageFrame3)
        display3.imgtk = tkimage3
        display3.configure(image=tkimage3)
        display3.grid()
    except Exception as e:
        print(e)
        noti = tk.Label(tk_window, text='Carregue uma imagem primeiro', width=33, height=1, fg="white", bg="black",
                        font=('times', 15, ' bold '))
        noti.place(x=240, y=500)
        tk_window.after(5000, destroy_widget, noti)


def save_img():
    try:
        global noti, dna
        ts = datetime.datetime.now()
        current_date = ts.strftime("%Y-%m-%d_%H-%M-%S")
        filename = "{}_filter.jpg".format(current_date)
        op.save('./Captures/' + filename)

        dna = tk.Label(tk_window, text='Imagem salva em /Captures', width=33, height=1, fg="black", bg="spring green",
                       font=('times', 15, ' bold '))
        dna.place(x=240, y=500)
        tk_window.after(5000, destroy_widget, dna)
    except:
        noti = tk.Label(tk_window, text='Problema ao salvar as imagens', width=33, height=1, fg="white", bg="black",
                        font=('times', 15, ' bold '))
        noti.place(x=240, y=500)
        tk_window.after(5000, destroy_widget, noti)


def leave():
    from tkinter import messagebox
    if messagebox.askokcancel("Sair", "Você deseja sair?"):
        tk_window.destroy()


def destroy_widget(widget):
    widget.destroy()


#
#   RENDERS ---- visual
#

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
                font=('times', 16, 'italic bold '), command=lambda: apply_ai(nl.load('intelligence_prot.net')))
med.place(x=700, y=280)
# BOTÃO DE PROTANOPIA

# BOTÃO DE DEUTERANOPIA
med = tk.Button(tk_window, borderwidth=0, bg='#1e88e5', fg="white", width=11, text='Deuteranopia',
                font=('times', 16, 'italic bold '), command=lambda: apply_ai(nl.load('intelligence_deut.net')))
med.place(x=700, y=360)
# BOTÃO DE DEUTERANOPIA

# BOTÃO DE TRITANOPIA
med = tk.Button(tk_window, borderwidth=0, bg='#1e88e5', fg="white", width=11, text='Tritanopia',
                font=('times', 16, 'italic bold '), command=lambda: apply_ai(nl.load('intelligence_trit.net')))
med.place(x=700, y=440)
# BOTÃO DE TRITANOPIA


names = tk.Label(tk_window, text="© Developed by Felipe E. Schmidt ©", bg="#616161", fg="white", width=67,
                 height=2, font=('times', 30, 'italic bold '))
names.place(x=00, y=740)

tk_window.protocol("WM_DELETE_WINDOW", leave)
tk_window.mainloop()