from tkinter import *
import os
from tkinter.messagebox import showwarning, showerror
import hashlib


class Login_Media_Library():

    def __init__(self, accessWindow):

        '''Creamos una interfaz con  dos botones unicamente'''

        self.accessWindow=accessWindow
        self.accessWindow.title ('ACCESO A LA HEMEROTECA')
        self.accessWindow.geometry('350x250+600+50')
        self.accessWindow.config(bg='light slate grey')
  
        self.login_button= Button(self.accessWindow,text='Acceso',font=('Verdana',12), bd=5, command=self.login).place(x=130,y=70)
        self.registration_button= Button(self.accessWindow, text='Registro', font=('Verdana',12), bd=5, command=self.registration).place(x=130,y=140)    


    def check_thesame(self):

        '''Creamos la lista de los nombres de usuario habilitados por la hemeroteca. Si el nombre de usuario introducido se encuentra en la lista,
        comprobamos que las dos contrasenias introducidas sean iguales, si lo son le informamos de que hemos guardado su contrasenia
        y si no le pedimos que vuelva a probar. Si introduce usuario no habilitado, le informamos.'''
       
        
        User_list=[]
        for i in range(1,16):
            User_list.append('Prueba'+str(i))
        if user.get() in User_list:

            crypted_user=hashlib.sha512((user.get()).encode('utf-8')).hexdigest()
            crypted_password=hashlib.sha512((password1.get()).encode('utf-8')).hexdigest()
        
            try:
                open(user.get(),'r')
                showwarning (title='CUIDADO', message='Ese nombre de usuario ya tiene una password elegida.')
                
            except Exception as isnew:
                if (self.password_entry1.get()== self.password_entry2.get()):
                    file=open(user.get(),'w')
                    file.write (crypted_user+ '\n'+ crypted_password)
                    file.close()
                    showwarning (title='PASSWORD GUARDADA CON EXITO', message='Ya puedes pinchar en "Acceso".')
                    self.registrationWindow.destroy()

                else:
                    showerror (title='ATENCION. PRUEBA OTRA VEZ.', message='Las passwords no coinciden. Vuelve a probar.')
                    self.registrationWindow.destroy()
                        
        else:
            showerror(title='ATENCION. PRUEBA OTRA VEZ.', message='Me has dado un nombre de usuario no habilitado como trabajador. '+
                        'Vuelve a probar en "Registro". ')
            self.registrationWindow.destroy()
            
    def registration(self):
        '''Creamos una ventana saliente nueva donde pedimos que se registre. La interfaz muestra un campo de entrada de usuario y
        dos de contrasenia para confirmarla. Y por ultimo un boton para guardar'''
        
        global registrationWindow
        global password_entry1, password_entry2, user_entry
        global user,password1, password2
        user=StringVar()
        password1=StringVar()
        password2=StringVar()
        self.registrationWindow=Toplevel(self.accessWindow)
        self.registrationWindow.title('ESCRIBIR USUARIO Y SELECCIONAR PASSWORD:')
        self.registrationWindow.geometry ('440x300+600+50')
        self.registrationWindow.config(bg='light slate grey')

        self.user_label=Label(self.registrationWindow,text='Usuario: ',font=('Verdana',8)).place (x=50,y=50)
        self.password_label=Label (self.registrationWindow, text='Password: ', font=('Verdana',8)).place(x=50,y=100)
        self.password_label2=Label (self.registrationWindow, text='Repite Password: ', font=('Verdana',8)).place(x=50,y=150)
        
        self.user_entry= Entry (self.registrationWindow, textvariable=user,font=('Verdana',8))
        self.user_entry.place(x=200,y=50)
        self.password_entry1=Entry (self.registrationWindow,textvariable=password1,font=('Verdana',8), show='*')
        self.password_entry1.place(x=200,y=100)
        self.password_entry2=Entry (self.registrationWindow,textvariable=password2,font=('Verdana',8), show='*')
        self.password_entry2.place(x=200,y=150)
        
        self.save_button= Button (self.registrationWindow, text='Guardar password', font=('Verdana',12), bd=5, command=self.check_thesame).place(x=200,y=220)


    def access(self):

        '''Pedimos que si el username coincide con uno de los habilitados de la lista primera,
        nos abra el fichero que tiene ese mismo nombre que el usuario y lo lea. Si la contrasenia guardada que es variable global
        esta en lo que lee, accedemos.
        Y se nos cierran todas las ventanas. Sino le denegamos el acceso y le explicamos porque.'''
        
        encrypted_registered_password= hashlib.sha512((registered_user.get()).encode('utf-8')).hexdigest()
        directory_list= os.listdir()
        if registered_user.get() in directory_list:
            file1=open(registered_user.get(),'r')
            check_key= file1.read().splitlines()
       
            if encrypted_registered_password in check_key:
                self.loginWindow.destroy()
                self.accessWindow.destroy()
                from MediaLibraryModules import mainMediaLibrary 
                
            else:
                showerror(title='ACCESO DESESTIMADO', message='La password es INCORRECTA')
                self.loginWindow.destroy()
        else:
            showerror(title='ACCESO DESESTIMADO', message='El usuario es INCORRECTO')
            self.loginWindow.destroy()
                
    def login(self):

        '''Creamos la interfaz de logueo, con dos campos: usuario y contrasenia y el boton de aceptar.'''
        
        global loginWindow
        global user_entry
        global password_entry
        global registered_user
        registered_user= StringVar()
        global registered_password
        registered_password= StringVar()
         
        self.loginWindow=Toplevel(self.accessWindow)
        self.loginWindow.title('INTRODUCIR USUARIO Y PALABRA CLAVE:')
        self.loginWindow.geometry ('400x300+600+50')
        self.loginWindow.config(bg='light slate grey')

        self.user_label=Label(self.loginWindow,text='Usuario: ',font=('Verdana',8)).place (x=70,y=50)
        self.password_label=Label (self.loginWindow, text='Password: ', font=('Verdana',8)).place(x=70,y=100)
        self.user_entry= Entry (self.loginWindow, textvariable=registered_user ,font=('Verdana',8))
        self.user_entry.place(x=180,y=50)
        self.password_entry=Entry (self.loginWindow,textvariable=registered_password ,font=('Verdana',8), show='*')
        self.password_entry.place(x=180,y=100)
        self.accept_button=Button (self.loginWindow, text='Aceptar',font=('Verdana',10), bd=5, command=self.access).place(x=200,y=200)

   
root=Toplevel()
Login_Media_Library(root)
root.mainloop()
