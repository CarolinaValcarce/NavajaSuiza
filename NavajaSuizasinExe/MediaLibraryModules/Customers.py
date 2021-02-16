from tkinter import *
import sqlite3
from tkinter.messagebox import showwarning,showerror

class Customers():

    def __init__(self,master):
        self.master=master
        master.title('CONTACTOS DE CLIENTES DE LA HEMEROTECA')
        master.geometry('630x450+500+0')
        master.configure(bg='light slate grey')

        connection=sqlite3.connect('Hemeroteca.db')
        c= connection.cursor()
            
        '''Creamos el formulario con campos de texto y etiquetas y lo situamos en celdas grid.'''
        self.l_DNI=Label(master, text='DNI sin letra ni espacios:',bg='light slate grey',fg='white').grid(row=0, column=0, padx=5, pady=5)
        self.e_DNI= Entry (master, width=55)
        self.e_DNI.grid (row=0,column=1, columnspan=2)
        self.e_name=Entry(master, width=55)
        self.e_name.grid(row=1, column=1, columnspan=2)
        self.l_name=Label(master, text='Nombre: ',bg='light slate grey',fg='white').grid(row=1, column=0,padx=5, pady=5 )
        self.e_lastname=Entry(master, width=55)
        self.e_lastname.grid(row=2, column=1, columnspan=2)
        self.l_lastname=Label(master, text='Apellidos: ',bg='light slate grey',fg='white').grid(row=2, column=0,padx=5, pady=5)
        self.l_address=Label(master, text='Direccion: ',bg='light slate grey',fg='white').grid(row=3, column=0,padx=5, pady=5)
        self.e_address=Entry(master, width=55)
        self.e_address.grid(row=3, column=1,columnspan=2 )
        self.e_zipcode=Entry(master, width=55)
        self.e_zipcode.grid(row=4, column=1,columnspan=2 )

        self.l_zipcode=Label(master, text='Codigo postal: ',bg='light slate grey',fg='white').grid(row=4, column=0,padx=5, pady=5)
        self.l_city=Label(master, text='Ciudad: ',bg='light slate grey',fg='white').grid(row=5, column=0,padx=5, pady=5)
        self.e_city=Entry(master, width=55)
        self.e_city.grid(row=5, column=1,columnspan=2 )
        self.l_phone=Label(master, text='Telefono: ',bg='light slate grey',fg='white').grid(row=6, column=0,padx=5, pady=5)
        self.e_phone=Entry(master, width=55)
        self.e_phone.grid(row=6, column=1,columnspan=2)
        self.e_email=Entry(master, width=55)
        self.e_email.grid(row=7, column=1,columnspan=2 )
        self.l_email=Label(master, text='E-mail: ',bg='light slate grey',fg='white').grid(row=7, column=0,padx=5, pady=5 )

        self.b_send= Button (master, text='Guardar datos', bd=5,command=self.save).grid(row=8, column=0, columnspan=2,padx=5, pady=5)
        self.b_query= Button (master, text='Consultar datos',bd=5, command=self.query).grid(row=9, column=0, columnspan=2,padx=5, pady=5)
        self.e_selection= Entry (master, width=20)
        self.e_selection.grid(row=10, column=1)
        self.l_selection=Label(master, text='Elegir DNI:',bg='light slate grey', fg='white').grid(row=10, column=0)
        self.b_delete=Button(master, text= 'Borrar datos', bd=5,command=self.delete).grid(row=10, column=2,padx=5, pady=5)
        self.b_edit=Button(master, text='Actualizar datos',bd=5, command=self.edit).grid(row=9, column=2, columnspan=1, padx=5, pady=5)
        '''Creamos una etiqueta para destruirla cada vez que entremos en la funcion query, y construir una nueva para no sobreescribir los datos en la misma.'''
        global l_query
        self.l_query=Label(self.master)
        
        connection.close()

    def save(self):

        '''Creamos una conexion a bd llamada Hemeroteca que creamos en sqlite (previamente importada la libreria) y
        crear una tabla posicionando cursor en 0.'''
        try:
            connection=sqlite3.connect('Hemeroteca.db')
            c= connection.cursor()
            #c.execute ('DROP TABLE Clientes')
            c.execute ('PRAGMA foreign_keys=ON')
            c.execute ('''CREATE TABLE IF NOT EXISTS Clientes(DNI INTEGER PRIMARY KEY,nombre TEXT, apellidos TEXT,
                        direccion TEXT, codigo_postal INTEGER,
                        ciudad TEXT, telefono INTEGER, email TEXT)''')


            '''Insertamos los datos en la tabla creada usando query SQL.
            Capturamos mensajes de error si no se introducen DNI de 8 digitos o NIE de 7, si el codigo postal no es de 5.
            Si el telefono no es de 9 digitos o si el email no contiene punto o arroba.'''
            
            DNI=self.e_DNI.get()
            code=self.e_zipcode.get()
            phone=self.e_phone.get()
            email=self.e_email.get()
            if((len(code)==5 and code.isdigit())and (len(DNI)==8 or len(DNI)==7)):
                if ((('@' in email) and ('.'in email))and (len(phone)==9 and phone.isdigit())):
                    c.execute('INSERT INTO Clientes VALUES(?,?,?,?,?,?,?,?)',
                      (self.e_DNI.get(),self.e_name.get(),self.e_lastname.get(), self.e_address.get(), self.e_zipcode.get(), self.e_city.get(), self.e_phone.get(),self.e_email.get()))
                else:
                    showerror(title= 'ATENCION!!', message='Los emails siempre contienen un "@" y un "." Y los telefonos son de 9 digitos(sin espacios).')
            else:
                showerror (title= 'ATENCION!!', message='Los codigos postales son de 5 digitos. Y el DNI esta formado por 8 digitos o 7 si es de extranjero.')

            '''Borramos los campos de entrada, una vez introducida la info.'''
            self.e_DNI.delete(0,END)
            self.e_name.delete(0,END)
            self.e_lastname.delete(0,END)
            self.e_address.delete(0,END)
            self.e_zipcode.delete(0,END)
            self.e_city.delete(0,END)
            self.e_phone.delete(0,END)
            self.e_email.delete(0,END)
            
            '''Hacemos el commit, para confirmar las operaciones'''
            connection.commit()
            
        except Exception as exct:
            showerror(title='ATENCION', message='Ya existe un cliente con ese DNI. Corrige el DNI erroneo antes')

        
    def query(self):

        '''Recogemos en una etiqueta la salida de los registros con una salto de linea entre cada registro.
        Metemos espacios para cuando sobreescribamos en la etiqueta con registros mas cortos, tras haber introducido largos.
        Recogemos la excepcion si no devuelve nada porque no haya nada.'''
        
        try:
            connection=sqlite3.connect('Hemeroteca.db')
            c= connection.cursor()
            c.execute ('PRAGMA foreign_keys=ON')
        
            c.execute('SELECT * FROM Clientes')
            records=c.fetchall()
            print(records)
            
            print_records=''
            for record in records:
                print_records+=str(record)+'\n'
            self.l_query.destroy()
            self.l_query=Label(self.master, text=print_records)
            self.l_query.grid(row=11,column=0, columnspan=3)

            connection.commit()

        except Exception as ex:
            showwarning (title='ATENCION', message='Todavia no existe ningun cliente.')



    def delete(self):
        '''Recogemos la excepcion al borrar un registro que es cuando no haya seleccionado previamente que registro'''

        try:
            connection=sqlite3.connect('Hemeroteca.db')
            c= connection.cursor()
            c.execute ('PRAGMA foreign_keys=ON')
        
            c.execute('DELETE FROM Clientes WHERE DNI='+self.e_selection.get())
        except Exception as e:
            showwarning(title='ATENCION!!!', message='Da "Consultar datos" y selecciona un cliente existente en "Elegir DNI", antes de presionar "Borrar datos".')
        self.e_selection.delete(0,END)
        connection.commit()

    def update(self):

        '''Actualizamos los datos de la tabla con los valores globales recogidos de los campos de la interfaz creada en la funcion edit que es para editar los datos.
        Y suponiendo que cumpla los requisitos previos de numero de digitos o contenido del email. Cerramos la ventana del editor.'''
      
        connection=sqlite3.connect('Hemeroteca.db')
        c= connection.cursor()
        c.execute ('PRAGMA foreign_keys=ON')
        DNI_editor=self.e_DNI_editor.get()
        code_editor=self.e_zipcode_editor.get()
        phone_editor=self.e_phone_editor.get()
        email_editor=self.e_email_editor.get()
        if((len(code_editor)==5 and code_editor.isdigit())and (len(DNI_editor)==8 or len(DNI_editor)==7)):
            if ((('@' in email_editor) and ('.'in email_editor)) and (len(phone_editor)==9 and phone_editor.isdigit())):
                 c.execute('UPDATE Clientes SET DNI=(?),nombre=(?),apellidos=(?),direccion=(?),codigo_postal=(?),ciudad=(?),telefono=(?),email=(?) WHERE DNI=(?)',
                  (self.e_DNI_editor.get(),self.e_name_editor.get(),self.e_lastname_editor.get(),self.e_address_editor.get(),self.e_zipcode_editor.get(),
                   self.e_city_editor.get(),self.e_phone_editor.get(),self.e_email_editor.get(),self.e_selection.get()))  
            else:
                showwarning(title= 'ATENCION!!', message='Los emails siempre contienen un "@" y un "." Y los telefonos son de 9 digitos sin espacios.')
        else:
            showwarning (title= 'ATENCION!!', message='Los codigos postales son de 5 digitos. Y el DNI contiene 8 digitos o 7 si es de extranjero.')

       
        connection.commit()

        self.editor.destroy()

    def edit(self):

        global e_DNI_editor
        global e_name_editor
        global e_lastname_editor
        global e_address_editor
        global e_zipcode_editor
        global e_city_editor
        global e_phone_editor
        global e_email_editor

        try:
            '''Seleccionamos los valores del registro cuando su primary key es igual a la que nos dan, para rellenar todos los campos de la interfaz
            de edicion, con los datos existentes y insertamos un boton de guardar, para que nos lleve a la funcion de aceptar los cambios realizados'''
            
            connection=sqlite3.connect('Hemeroteca.db')
            c= connection.cursor()
            c.execute ('PRAGMA foreign_keys=ON')
        
            c.execute('SELECT * FROM Clientes WHERE DNI='+self.e_selection.get())
            records=c.fetchall()

            global editor
            self.editor=Tk()
            self.editor.title('ACTUALIZAR DATOS DE CONTACTO:')
            self.editor.geometry('500x320+550+0')
            self.editor.configure(bg='light slate grey')

            self.l_DNI_editor=Label(self.editor, text='DNI sin letra ni espacios:',bg='light slate grey',fg='white').grid(row=0, column=0, padx=5, pady=5)
            self.e_DNI_editor= Entry (self.editor, width=55)
            self.e_DNI_editor.grid (row=0,column=1, columnspan=2)
            
            self.e_name_editor=Entry(self.editor, width=55)
            self.e_name_editor.grid(row=1, column=1, columnspan=2)
            self.l_name_editor=Label(self.editor, text='Nombre: ',bg='light slate grey',fg='white').grid(row=1, column=0,padx=5, pady=5 )
            self.e_lastname_editor=Entry(self.editor, width=55)
            self.e_lastname_editor.grid(row=2, column=1, columnspan=2)
            self.l_lastname_editor=Label(self.editor, text='Apellidos: ',bg='light slate grey',fg='white').grid(row=2, column=0,padx=5, pady=5)
            self.l_address_editor=Label(self.editor, text='Direccion: ',bg='light slate grey',fg='white').grid(row=3, column=0,padx=5, pady=5)
            self.e_address_editor=Entry(self.editor, width=55)
            self.e_address_editor.grid(row=3, column=1,columnspan=2 )
            self.e_zipcode_editor=Entry(self.editor, width=55)
            self.e_zipcode_editor.grid(row=4, column=1,columnspan=2 )
            self.l_zipcode_editor=Label(self.editor, text='Codigo postal: ',bg='light slate grey',fg='white').grid(row=4, column=0,padx=5, pady=5)
            self.l_city_editor=Label(self.editor, text='Ciudad: ',bg='light slate grey',fg='white').grid(row=5, column=0,padx=5, pady=5)
            self.e_city_editor=Entry(self.editor, width=55)
            self.e_city_editor.grid(row=5, column=1,columnspan=2 )
            self.l_phone_editor=Label(self.editor, text='Telefono: ',bg='light slate grey',fg='white').grid(row=6, column=0,padx=5, pady=5)
            self.e_phone_editor=Entry(self.editor, width=55)
            self.e_phone_editor.grid(row=6, column=1,columnspan=2)
            self.e_email_editor=Entry(self.editor, width=55)
            self.e_email_editor.grid(row=7, column=1,columnspan=2 )
            self.l_email_editor=Label(self.editor, text='E-mail: ',bg='light slate grey',fg='white').grid(row=7, column=0,padx=5, pady=5 )
            

            for record in records:
                self.e_DNI_editor.insert(0,record[0])
                self.e_name_editor.insert(0,record[1])
                self.e_lastname_editor.insert(0, record[2])
                self.e_address_editor.insert(0, record[3])
                self.e_zipcode_editor.insert(0,record[4])
                self.e_city_editor.insert(0, record[5])
                self.e_phone_editor.insert(0,record[6])
                self.e_email_editor.insert(0, record[7])
                
            self.b_update=Button(self.editor, text='Actualizar datos', command=self.update, bd=5).grid(row=8, column=0, columnspan=3,padx=5, pady=5)

            connection.commit()
            

        except Exception as exc:
            showwarning(title='ATENCION!!', message='Da "Consultar datos" y selecciona un cliente existente en "Elegir DNI", antes de presionar "Actualizar datos".')

r=Tk()
Customers(r)
r.mainloop()

