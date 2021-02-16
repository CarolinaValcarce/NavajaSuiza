from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import os, sys
from tkinter.messagebox import showwarning, showerror
import pathlib

class NavajaSuiza:

    def __init__(self,master):

        self.master=master
        master.title('La Navaja Suiza')
        master.geometry('350x430')

        '''Usamos de fondo en la ventana una imagen que incorporamos en la etiqueta con ruta relativa
        para cuando creemos el ejecutable que no se pierda. E incorporamos 5 botones que reenvian a clases del paquete Modulos.'''

        self.image_path= pathlib.Path(__file__).absolute().parent/'Modulos/imag/Portada1.png'   
        self.background_image= ImageTk.PhotoImage(Image.open(self.image_path))
        self.background_label = Label(master, image=self.background_image).place(x=0,y=0)

        self.Button1=Button (master, text='Hemeroteca', bd=5, command= self.media_Library).place(x=30, y=50)
        self.Button2=Button (master, text='Calculadora', bd=5,command= self.calculator).place(x=30, y=100)
        self.Button3=Button (master, text='Acceder a fotos', bd=5, command= self.openDirectory).place(x=30, y=150)
        self.Button4=Button (master, text='Tiempo', bd=5, command= self.weatherApi).place(x=30,y=200)
        self.Button5=Button (master, text='Juego', bd=5, command= self.game).place(x=30,y=250)
        

    def calculator(self):
        from Modulos import Calculator


    def openDirectory(self):

        '''Abrimos una dialogo del fichero imagenes incorporandolo en una etiqueta con la opcion de seleccionar ficheros:
        .png, .jpg, o todo tipo de ficheros. Y a su vez, incorporamos las imagenes en otra etiqueta.'''
        
        global myImages
        self.root_path= pathlib.Path(__file__).absolute().parent/'Modulos/imag'  
        self.filename=filedialog.askopenfilename(initialdir=self.root_path,title="Directorio fotos",
                                                   filetypes=(("ficheros jpg","*.jpg"),("ficheros png","*.png"),("cualquier fichero","*.*")))
        self.MainLabel= Label(root, text=self.filename).pack()
        self.myImages= ImageTk.PhotoImage (Image.open(self.filename))
        self.ImagesLabel= Label (image=self.myImages).pack()


    def game(self):
        from Modulos import Game
        
    def weatherApi(self):
        
        from Modulos import WeatherApi
        
    def media_Library(self):

        from Modulos import Login_Media_Library



root=Tk()
NavajaSuiza(root)

root.mainloop()

