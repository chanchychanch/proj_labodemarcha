# -*- coding: cp1252 -*-
import cv2
import PIL.Image
import PIL.ImageTk
import Tkinter as tk
import ttk
import time


def update_image(image_label, cv_capture, flagREC, cv_out):
    cv_image = cv_capture.read()[1]
    if flagREC[0] == 1:
        a.configure(text = "Grabando secuencia de video...")
        cv_out.write(cv_image)
    else:
        a.configure(text = "Esperando") 
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    pil_image = PIL.Image.fromarray(cv_image)
    #pil_image.save('image3.jpg')
    tk_image = PIL.ImageTk.PhotoImage(image=pil_image)
    image_label.configure(image=tk_image)
    image_label._image_cache = tk_image  # avoid garbage collection
    root.update()    

def update_all(root, image_label, cv_capture, flagREC, cv_out):
    if root.quit_flag:
        root.destroy()  # this avoids the update event being in limbo
    else:
        update_image(image_label, cv_capture, flagREC, cv_out)
        root.after(10, func=lambda: update_all(root, image_label, cv_capture, flagREC, cv_out))

def Play():
    a = tk.Label(frame_img, text = "Play")
    a.grid(column=0, row=2)

def Pause():
    a = tk.Label(frame_img, text = "Pause")
    a.grid(column=0, row=2)

def Stop(cv_out, flagREC):
    flagREC[0] = False
    cv_out.release()

def Rec(cv_out, fourcc, flagREC):
    if cv_out.isOpened() == False:
        cv_out.open('output.avi',fourcc, 7.0, (640,480))    
    flagREC[0] = True

def select_cant_marcadores():
    selection = "Cantidad de marcadores: " + str(cant_marcadores.get())
    label_cant.config(text = selection)
    #cv2.rectangle(tk_image,(10,10),(100,100))
    rect1 = tk.Canvas(frame_img_marcadores, width = 30, height = 30)
    rect1.grid(column = 0, row = 0)
    square1 = rect1.create_rectangle(0,0,25,25, fill="green")
    rect2 = tk.Canvas(frame_img_marcadores, width = 30, height = 30)
    rect2.grid(column = 0, row = 1)
    square2 = rect2.create_rectangle(0,0,25,25, fill="red")
    rect3 = tk.Canvas(frame_img_marcadores, width = 30, height = 30)
    rect3.grid(column = 0, row = 2)
    square3 = rect3.create_rectangle(0,0,25,25, fill="blue")
    if cant_marcadores.get() != 3:
        rect4 = tk.Canvas(frame_img_marcadores, width = 30, height = 30)
        rect4.grid(column = 0, row = 3)
        square4 = rect4.create_rectangle(0,0,25,25, fill="violet")
        if cant_marcadores.get() != 4:
            rect5 = tk.Canvas(frame_img_marcadores, width = 30, height = 30)
            rect5.grid(column = 0, row = 4)
            square5 = rect5.create_rectangle(0,0,25,25, fill="yellow")


if __name__ == '__main__':
    cv_capture = cv2.VideoCapture()
    cv_capture.open(0)  # have to use whatever your camera id actually is
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    cv_out = cv2.VideoWriter('output.avi',fourcc, 7.0,(640,480))
    root = tk.Tk()
    root.title("OnkyLab")
    root.option_add('*tearOff', tk.FALSE)

    flagREC = [False];

    tabs = ttk.Notebook(root) 
    tabs.pack(fill='both', expand=1) 
    tab_adquisicion = ttk.Frame(tabs) 
    tabs.add(tab_adquisicion, text='Adquisición') 
    tab_resultados = ttk.Frame(tabs) 
    tabs.add(tab_resultados, text='Resultados') 

    
    #Para hacer el menu

    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Nuevo") #, command=donothing)
    filemenu.add_command(label="Abrir")
    filemenu.add_command(label="Guardar")
    filemenu.add_command(label="Guardar como...")
    filemenu.add_command(label="Cerrar")
    filemenu.add_separator()
    filemenu.add_command(label="Salir")
    menubar.add_cascade(label="Arhivo", menu=filemenu)
    
    editmenu = tk.Menu(menubar, tearoff=0)
    editmenu.add_command(label="Atrás")
    editmenu.add_separator()
    editmenu.add_command(label="Cortar")
    editmenu.add_command(label="Copiar")
    editmenu.add_command(label="Pegar")
    editmenu.add_command(label="Borrar")
    editmenu.add_command(label="Seleccionar todo")
    menubar.add_cascade(label="Editar", menu=editmenu)
    
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index")
    helpmenu.add_command(label="About...")
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)
    
    #Creo los dos frames generales
    frame_datos = tk.Frame(tab_adquisicion, width = 200, height = 200, borderwidth = 2, relief = 'sunken')
    frame_datos.grid(column = 0, row = 0, sticky = tk.N, padx = 5, pady = 5)
    frame_img = tk.Frame(tab_adquisicion, borderwidth = 2, relief = 'sunken')
    frame_img.grid(column = 1, row = 0, padx = 5, pady = 5)

    frame_img_marcadores = tk.Frame(frame_img, borderwidth = 2, relief = 'sunken')
    frame_img_marcadores.grid(column = 1, row = 0, padx = 5, pady = 5)
    frame_img_botones = tk.Frame(frame_img, borderwidth = 2, relief = 'sunken')
    frame_img_botones.grid(column = 0, row = 2, padx = 5, pady = 5)

    setattr(root, 'quit_flag', False)
    def set_quit_flag():
        root.quit_flag = True
    root.protocol('WM_DELETE_WINDOW', set_quit_flag)  # avoid errors on exit
    

    #Frame con el video
    image_label = tk.Label(frame_img)  # the video will go here
    image_label.grid(column = 0, row = 0)

    scroll = tk.Scrollbar(frame_img, orient=tk.HORIZONTAL)
    scroll.grid(column = 0, row = 1)
    img_play = tk.PhotoImage(file="Play.gif")
    bot_play = tk.Button(frame_img_botones, text = "Play", image = img_play, compound = "top", command = Play)
    bot_play.grid(column = 0, row = 1)
    img_pause = tk.PhotoImage(file="Pause.gif")
    bot_pause = tk.Button(frame_img_botones, text = "Pause", image = img_pause, compound = "top", command = Pause)
    bot_pause.grid(column = 1, row = 1)
    img_stop = tk.PhotoImage(file="Stop.gif")
    bot_stop = tk.Button(frame_img_botones, text = "Stop", image = img_stop, compound = "top", command = lambda: Stop(cv_out, flagREC))
    bot_stop.grid(column = 2, row = 1)
    img_rec = tk.PhotoImage(file="Rec.gif")
    bot_rec = tk.Button(frame_img_botones, text = "Rec", image = img_rec, compound = "top", command = lambda: Rec(cv_out, fourcc, flagREC))
    bot_rec.grid(column = 3, row = 1)

    #a: nombre feo de un label que está abajo de los botones:
    a = tk.Label(frame_img, text = "Esperando")
    a.grid(column=0, row=3)

    #Frame de los datos
    label_nombre = tk.Label(master = frame_datos, text = "Nombre: ")
    label_nombre.grid(column = 0, row = 0, sticky = tk.W, padx = 5, pady = 5)
    label_apellido = tk.Label(master = frame_datos, text = "Apellido: ")
    label_apellido.grid(column = 0, row = 1, sticky = tk.W, padx = 5, pady = 5)
    label_edad = tk.Label(master = frame_datos, text = "Edad: ")
    label_edad.grid(column = 0, row = 2, sticky = tk.W, padx = 5, pady = 5)
    label_altura = tk.Label(master = frame_datos, text = "Altura: ")
    label_altura.grid(column = 0, row = 3, sticky = tk.W, padx = 5, pady = 5)
    label_peso = tk.Label(master = frame_datos, text = "Peso: ")
    label_peso.grid(column = 0, row = 4, sticky = tk.W, padx = 5, pady = 5)
    label_peso = tk.Label(master = frame_datos, text = "Fecha: ")
    label_peso.grid(column = 0, row = 5, sticky = tk.W, padx = 5, pady = 5)
    label_cant = tk.Label(master = frame_datos, text = "Cantidad de marcadores: ")
    label_cant.grid(column = 0, row = 6, sticky = tk.W, padx = 5, pady = 5)
    
    nombre = "Carolina"
    entry_nombre = tk.Entry(frame_datos, textvariable = nombre, width = 20)
    entry_nombre.grid(column = 1, row = 0, sticky = tk.W, padx = 5, pady = 5)
    entry_nombre.insert(0, nombre)
    apellido = "Fernandez"
    entry_apellido = tk.Entry(frame_datos, textvariable = apellido, width = 30)
    entry_apellido.grid(column = 1, row = 1, sticky = tk.W, padx = 5, pady = 5)
    entry_apellido.insert(0, apellido)
    edad = "25"
    entry_edad = tk.Entry(frame_datos, textvariable = edad, width = 7)
    entry_edad.grid(column = 1, row = 2, sticky = tk.W, padx = 5, pady = 5)
    entry_edad.insert(0, edad)
    altura = "1,70"
    entry_altura = tk.Entry(frame_datos, textvariable = altura, width = 10)
    entry_altura.grid(column = 1, row = 3, sticky = tk.W, padx = 5, pady = 5)
    entry_altura.insert(0, altura)
    peso = "54"
    entry_peso = tk.Entry(frame_datos, textvariable = peso, width = 7)
    entry_peso.grid(column = 1, row = 4, sticky = tk.W, padx = 5, pady = 5)
    entry_peso.insert(0, peso)
    fecha = time.localtime(time.time())
    dia = str(fecha.tm_mday)+"/"+str(fecha.tm_mon)+"/"+str(fecha.tm_year)
    entry_fecha = tk.Entry(frame_datos, textvariable = dia, width = 10)
    entry_fecha.grid(column = 1, row = 5, sticky = tk.W, padx = 5, pady = 5)
    entry_fecha.insert(0, dia)

    cant_marcadores = tk.IntVar()
    tres = ttk.Radiobutton(frame_datos, text = "3", variable = cant_marcadores, value = 3, command = select_cant_marcadores)
    tres.grid(column = 1, row = 6, sticky = tk.W, padx = 5, pady = 5)
    cuatro = ttk.Radiobutton(frame_datos, text = "4", variable = cant_marcadores, value = 4, command = select_cant_marcadores)
    cuatro.grid(column = 1, row = 7, sticky = tk.W, padx = 5, pady = 5)
    cinco = ttk.Radiobutton(frame_datos, text = "5", variable = cant_marcadores, value = 5, command = select_cant_marcadores)
    cinco.grid(column = 1, row = 8, sticky = tk.W, padx = 5, pady = 5)

    tres.invoke() #Por default se marca 3
    
    root.after(0, func=lambda: update_all(root, image_label, cv_capture, flagREC, cv_out))
    root.mainloop()
    
    cv_capture.release() #Apago la cámara
    cv_out.release()
