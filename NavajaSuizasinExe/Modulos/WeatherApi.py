from tkinter import *
from PIL import ImageTk, Image
import json
import os,sys
import pathlib
import requests
from tkinter.messagebox import showwarning

class WeatherApi:

    def __init__(self,weather):

        self.weather=weather
        weather.geometry('500x350+550+50')
        weather.config (bg='tan')
        weather.title('Api del Tiempo')

        '''#Capturamos la excepcion con un mensaje de error por si no conseguimos la conexion a la web del tiempo.
        #En la variable api incluimos en un json la respuesta de la api web. Creamos variables para recoger cada uno de los valores del json.
        #La temperatura nos la provee la web en Kelvin y la pasamos a Celsius.
        Redondeamos la temperatura trasformada a Celsius para que no nos aparezcan 7 u 8 decimales.
        #Creamos etiquetas para incorporar los datos obtenidos. Y usamos place para darnos total eleccion de donde colocarlo.
        No querriamos un formato tipo tabla 'grid()' ni un 'pack().

        Creamos las etiquetas que mostraran las caracteristicas de la ciudad seleccionada, fuera de la funcion llamada en donde se crean,
        ya que en esa funcion antes de crearlas procedemos a borrarlas.
        Asi cada vez que seleccionemos una nueva ciudad no sobreescribira el texto en la misma etiqueta sino que creara de nuevo las etiquetas.'''
        
        self.mylabel=Label(self.weather)
        self.firstlabel=Label(self.weather)
        self.secondlabel=Label(self.weather)
        self.thirdlabel=Label(self.weather)

        try:
            api_request=requests.get('http://api.openweathermap.org/data/2.5/weather?q=Valladolid,spain&APPID=0086c89433ebf8c843db3045575d0823&lang=es')
            api=json.loads(api_request.content)
            coordinates= api['coord']
            main_description= api ['weather'][0]['main']
            description=api['weather'][0]['description']
            temperature=api['main']['temp']
            temperatureC=DoubleVar()
            temperatureC=round((temperature-273.15),1)
            humidity=api['main']['humidity']
            city=api['name']
            
            self.Valladolid=Label(weather, text=('Ciudad: '+city), font=('Arial',15), bg='tan', fg='black' ).place(x=15, y=15)
            self.coord=Label(weather,text=('Coordenadas: '+str(coordinates)),font=('Arial',15), bg='tan', fg='black' ).place(x=15, y=40)
            self.temp=Label(weather, text=('Descripcion: '+description+ '. Temperatura: '+ str(temperatureC)+'*C'),font=('Arial',15), bg='tan', fg='black').place(x=15, y=65)
            self.humedity=Label(weather, text=('Humedad: '+ str(humidity)+'%'),font=('Arial',15), bg='tan', fg='black').place(x=120, y=90)
                
            '''Ahora escogemos la variable original en ingles del json recibido para declarar la eleccion de imagenes
            que se mostraran dependiendo de los 5 valores que puede tomar la variable.
            Los 5 valores estan definidos en la documentacion de la api dependiendo del tiempo que haga: Nuboso, despejado, lluvia, tormenta o nieve.'''
            
            if main_description== 'Clear':
                rootpath= pathlib.Path(__file__).absolute().parent/'imag/Clear.png'
            elif main_description== 'Clouds': 
                rootpath= pathlib.Path(__file__).absolute().parent/'imag/Clouds.png'
            elif ((str(api['weather'][0]['id'])).startswith('7')):
                rootpath= pathlib.Path(__file__).absolute().parent/'imag/Foggy.png'    
            elif main_description== 'Rain' or 'Drizzle':
                rootpath= pathlib.Path(__file__).absolute().parent/'imag/Rain.png' 
            elif main_description== 'Snow': 
                rootpath= pathlib.Path(__file__).absolute().parent/'imag/Snow.png' 
            elif main_description== 'Thunderstorm':
                rootpath= pathlib.Path(__file__).absolute().parent/'imag/Thunderstorm.png'
            else:
                rootpath= pathlib.Path(__file__).absolute().parent/'imag/Exclamation.png'

            '''Hacemos global la variable mis imagenes para que las imagenes del tiempo puedan reconocerse en todo el modulo, fuera del metodo.
            Y creamos una etiqueta para contener a la imagen. Hemos creado rutas relativas para que no se pierdan al empaquetar el software.'''

            global myImages
            self.myImages= ImageTk.PhotoImage (Image.open(rootpath))
            self.ImagesLabel= Label (weather,image=self.myImages).place(x=15, y=100)
             
            
            self.e=Entry(weather,width=25)
            self.e.place(x=140, y=125)

            self.b= Button(weather,text='Selecciona la ciudad del Mundo', bd=5, command=self.select_city).place(x=140, y=155)
            self.breaklabel2= Label(weather, text='************',font=('Arial',15), bg='tan', fg='black').place(x=15, y=163)
            self.breaklabel3= Label (weather, text='*******************',font=('Arial',15), bg='tan', fg='black').place(x=315, y=110)

            '''Recogemos la excepcion con un catch. Si no se conecta internet o no reconoce las imagenes,
            o la website esta fuera de servicio nos saldra el mensaje.'''

        except Exception as e:
            api='Error. O la conexion internet no va o la web meteorologica esta fuera de servicio...'
            self.mylabel=Label(weather, text=api).place(x=15, y=325)


        '''Creamos una segunda funcion dentro de la clase del tiempo para recibir el tiempo de cualquier ciudad del mundo que seleccione el usuario.
        No es sensitivo a mayusculas o minusculas, y acepta hasta pueblos.'''
    def select_city(self):

        try:
            cityselected=self.e.get()
            url='http://api.openweathermap.org/data/2.5/weather?q='+cityselected+',spain&APPID=0086c89433ebf8c843db3045575d0823&lang=es'
            api2=requests.get(url).json()
            coordinates= api2['coord']
            main_description= api2 ['weather'][0]['main']
            description=api2['weather'][0]['description']
            temperature=api2['main']['temp']
            temperatureC=DoubleVar()
            temperatureC=round((temperature-273.15),1)
            humidity=api2['main']['humidity']
            city=api2['name']

            '''Dado que cada vez que escribamos un sitio generara una salida y pueden ser muchas poblaciones,
            decido reusar la misma etiqueta. Hemos creado ya esas etiquetas en la clase fuera de la funcion. En la funcion cuando accedemos las cancelamos y las volvemos a crear de nuevo.
            Asi no se sobreescribe el texto uno encima de otro sino que creamos y destruimos la etiqueta cada vez.'''
            self.mylabel.destroy()
            self.firstlabel.destroy()
            self.secondlabel.destroy()
            self.thirdlabel.destroy()

            '''Rellenamos con los valoreas de la api dados para esa poblacion recreando las etiquetas.'''
            self.mylabel=Label( self.weather,text=('Ciudad: '+city), font=('Arial',15), bg='tan', fg='white' )
            self.mylabel.place(x=15, y=200)
            self.firstlabel=Label(self.weather,text=('Coordenadas: '+str(coordinates)),font=('Arial',15), bg='tan', fg='white' )
            self.firstlabel.place(x=15, y=225)
            self.secondlabel=Label(self.weather,text=('Descripcion: '+description+ '. Temperatura: '+ str(temperatureC)+'*C'),font=('Arial',15), bg='tan', fg='white')
            self.secondlabel.place(x=15, y=250)
            self.thirdlabel=Label(self.weather, text=('Humedad: '+ str(humidity)+'%'),font=('Arial',15), bg='tan', fg='white')
            self.thirdlabel.place(x=15,y=275)
            self.breaklabel=Label(self.weather,text='***********************',font=('Arial',15), bg='tan', fg='white').place(x=15, y=300)

            if main_description== 'Clear':
                rootpath= pathlib.Path(__file__).absolute().parent/'imag/Clear.png'  
            elif main_description== 'Clouds': 
                rootpath= pathlib.Path(__file__).absolute().parent/'imag/Clouds.png' 
            elif main_description== 'Rain' or 'Drizzle':
                rootpath= pathlib.Path(__file__).absolute().parent/'imag/Rain.png' 
            elif main_description== 'Snow': 
                rootpath= pathlib.Path(__file__).absolute().parent/'imag/Snow.png' 
            elif main_description== 'Thunderstorm':
                rootpath= pathlib.Path(__file__).absolute().parent/'imag/Thunderstorm.png'
            elif ((str(api['weather'][0]['id'])).startswith('7')):
                rootpath= pathlib.Path(__file__).absolute().parent/'imag/Foggy.png'
            else:
                rootpath= pathlib.Path(__file__).absolute().parent/'imag/Exclamation.png'    

            global myImages2
            self.myImages2= ImageTk.PhotoImage (Image.open(rootpath))
            self.ImagesLabel= Label (self.weather,image=self.myImages2).place(x=390, y=180)

            '''Recogemos la excepcion si por cualquier motivo introducimos una palabra inexistente o no se encuentra la ciudad'''

        except Exception as exc:
            api2='No hemos encontrado la ciudad.'
            showwarning(title='PRUEBA OTRA VEZ!!!!', message= api2)
        


root=Toplevel()
WeatherApi(root)
root.mainloop()
    

