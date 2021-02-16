from tkinter import *
import sqlite3
from tkinter.messagebox import showwarning, showerror

class Books():
    def __init__(self, r):

        '''Creamos el layout general. Con radiobutton, entradas de texto, entrada de texto multilineas, etiquetas y botones.''' 

        self.r=r
        r.title('LIBROS DISPONIBLES EN LA HEMEROTECA')
        r.geometry('500x490+550+0')
        r.configure(bg='light slate grey')

        connection=sqlite3.connect('Hemeroteca.db')
        c=connection.cursor()
        
        self.genre=StringVar()

        self.l_gnral=Label(r, text='FORMULARIO CON DATOS DE LIBROS:').grid(row=0, column=0,columnspan=3, padx=5, pady=5)
        self.e_ISBN=Entry(r,  width=55)
        self.e_ISBN.grid(row=1, column=1, columnspan=2)
        self.l_ISBN=Label(r, text='ISBN sin guiones: ',bg='light slate grey',fg='white').grid(row=1, column=0,padx=5, pady=5 )
        self.e_title=Entry(r, width=55)
        self.e_title.grid(row=2, column=1, columnspan=2)
        self.l_title=Label(r, text='Titulo:',bg='light slate grey',fg='white').grid(row=2, column=0,padx=5, pady=5)
        self.l_genre=Label(r, text='Genero:',bg='light slate grey',fg='white').grid(row=3, column=0,padx=5, pady=5)
        self.rb_genre1= Radiobutton(r, text='Aventuras', variable=self.genre, value='Aventuras').grid(row=4,column=0,  padx=5, pady=5)
        self.rb_genre2= Radiobutton(r, text='Cuentos de hadas', variable=self.genre,value='Cuentos de Hadas').grid(row=4,column=1,  padx=5, pady=5)
        self.rb_genre3= Radiobutton(r, text='Ciencia Ficcion', variable=self.genre,value='Ciencia Ficcion').grid(row=4,column=2,  padx=5, pady=5)
        self.rb_genre4= Radiobutton(r, text='Romantica', variable=self.genre, value='Romantica').grid(row=5,column=0,  padx=5, pady=5)
        self.rb_genre5= Radiobutton(r, text='Fantasia', variable=self.genre, value='Fantasia').grid(row=5,column=1,  padx=5, pady=5)
        self.rb_genre6= Radiobutton(r, text='Policiaca', variable=self.genre,value='Policiaca').grid(row=5,column=2, padx=5, pady=5)

        self.genre.get()

        self.e_author=Entry(r, width=55)
        self.e_author.grid(row=6, column=1,columnspan=2 )
        self.l_author=Label(r, text='Autor: ',bg='light slate grey',fg='white').grid(row=6, column=0,padx=5, pady=5)
        self.l_sinopsis=Label(r, text='Sinopsis: ',bg='light slate grey',fg='white').grid(row=7, column=0,padx=5, pady=5)
        self.e_sinopsis= Text(r, width=45, height=5)
        self.e_sinopsis.grid(row=7, column=1, columnspan=3, padx=5, pady=5 )


        self.b_send= Button (r, text='Guardar datos', bd=5,command=self.save).grid(row=14, column=0, columnspan=2,padx=5, pady=5)
        self.b_query= Button (r, text='Consultar datos',bd=5, command=self.query).grid(row=15, column=0, columnspan=2,padx=5, pady=5)
        self.e_selection= Entry (r, width=20)
        self.e_selection.grid(row=13, column=1)
        self.l_selection=Label(r, text='Elegir ISBN:',bg='light slate grey', fg='white').grid(row=13, column=0)
        self.b_delete=Button(r, text= 'Borrar datos', bd=5,command=self.delete).grid(row=14, column=2,padx=5, pady=5)
        self.b_edit=Button(r, text='Actualizar datos',bd=5, command=self.edit).grid(row=15, column=2, columnspan=1, padx=5, pady=5)
        self.labelRecords=Label(self.r)

        connection.close()

    def save(self):

        '''Abrimos la conexion y creamos una tabla insertando los datos que previamente nos ha rellenado el usuario,
        y una vez guardados, vaciamos los campos de entrada. Mostramos mensajes de error si el ISBN no es de 13 o ya existe''' 

        try:
            connection=sqlite3.connect('Hemeroteca.db')
            c=connection.cursor()
            c.execute('PRAGMA foreign_keys=ON')
            #c.execute('DROP TABLE Libros')
            c.execute('''CREATE TABLE IF NOT EXISTS Libros
                (ISBN INTEGER PRIMARY KEY, Titulo TEXT NOT NULL, Genero TEXT, Autor TEXT, Sinopsis TEXT)''')
            if (((self.e_ISBN.get()).isdigit) and len(self.e_ISBN.get())==13) and (self.e_title.get()!=''):

                c.execute('INSERT INTO Libros (ISBN, Titulo, Genero, Autor, Sinopsis) VALUES(?,?,?,?,?)',
                      (self.e_ISBN.get(),self.e_title.get(), self.genre.get(),self.e_author.get(),self.e_sinopsis.get(1.0,END)))
            
                self.e_ISBN.delete(0,END)
                self.e_title.delete(0,END)
                self.genre.set('Cuentos de hadas')
                self.e_author.delete(0,END)
                self.e_sinopsis.delete(1.0,END)

                connection.commit()
            else:
                showerror(title='ISBN NO CORRECTO', message='El ISBN debe contener 13 digitos. No introducir guiones, ni espacios. Y el titulo no puede estar vacio')

        except Exception as err:
             showerror(title='ATENCION', message='Ya existe un libro con ese ISBN. Corrige el ISBN erroneo antes.')


    def query(self):

        '''Conectamos a la bbdd y recogemos todos los registros. Los introducimos en una etiqueta separados entre ellos por salto de linea.
        Recogemos la excepcion si todavia no hay ningun registro.'''

        connection=sqlite3.connect('Hemeroteca.db')
        c=connection.cursor()
        c.execute('PRAGMA foreign_keys=ON')
        try:

            c.execute('SELECT ISBN, Titulo, Genero, Autor FROM Libros')
            
            records=c.fetchall()
            print(records)
            
            printrecords=''
            for record in records:
                printrecords+= str(record)+'\n'
            self.labelRecords.destroy()
            self.labelRecords=Label(self.r, text=printrecords)
            self.labelRecords.grid(row=16, column=0, columnspan=3)

        except Exception as e:
            showwarning(title='ATENCION', message='Todavia no hay ningun libro disponible.')

        connection.commit()

    def update(self):

        '''Conectamos con la bbdd  y actualizamos los valores de un registro con los proporcionados por el susuario en variables globales
        en la ventana edit. El registro escogido es donde el ISBN sea el que nos dio el usuario, en el layout general.
        Borramos el campo de entrada del ISBN proporcionado por el usuario.
        Y una vez hecho, cerramos la ventana de edicion.
        Recogemos con mensaje de error la posibilidad de que en la modificacion introduzca ISBN distinto de 13 digitos o el titulo vacio.'''
        
        connection=sqlite3.connect('Hemeroteca.db')
        c=connection.cursor()
        c.execute('PRAGMA foreign_keys=ON')
        if (((self.e_e_ISBN.get()).isdigit) and len(self.e_e_ISBN.get())==13) and (self.e_e_title.get()!=''):

            c.execute('UPDATE Libros SET ISBN=(?), Titulo=(?), Genero=(?), Autor=(?), Sinopsis=(?) WHERE ISBN=(?)',
                      (self.e_e_ISBN.get(), self.e_e_title.get(),self.editor_e_genre.get(),self.e_e_author.get(), self.e_e_sinopsis.get(1.0,END), self.e_selection.get()))
            self.e_selection.delete(0,END)
            connection.commit()
            self.editor.destroy()
        else:
            showerror(title='ISBN NO CORRECTO', message='El ISBN debe contener 13 digitos. No introducir guiones, ni espacios. Y el titulo no puede estar vacio')
    

    def delete(self):

        '''Conectamos con la bbdd y eliminamos de la tabla el registro cuyo ISBN sea el proporcionado por el usuario.
        Vaciamos el campo de entrada del ISBN y recogemos la excepcion si nos da un ISBN inexistente.'''
        
        connection=sqlite3.connect('Hemeroteca.db')
        c=connection.cursor()
        c.execute('PRAGMA foreign_keys=ON')
        try: 
            c.execute('DELETE FROM Libros WHERE ISBN='+self.e_selection.get())
        except Exception as e:
            showwarning(title='ATENCION!!!', message='Da "Consultar datos" y selecciona un cliente existente en "Elegir ISBN", antes de presionar "Borrar datos".')
        self.e_selection.delete(0,END)
        connection.commit()

    def new_chose(self):

        '''En la ventana de edicion incorporamos en el campo texto del genero de libro la opcion que seleccione el usuario con el radioButton.'''
        self.editor_e_genre.delete(0,END)
        self.editor_e_genre.insert(0,self.editor_genre.get())
        
        
    def edit(self):
      
        global editor
        global e_e_ISBN
        global e_e_title
        global editor_genre
        self.editor_genre=StringVar()
        global editor_e_genre
        global e_e_author
        global e_e_sinopsis
       
        '''Conectamos a la bbdd, creamos una ventana de edicion que provenga de la principal con Toplevel.
        Y rellenamos los campos de texto con los valores del registro donde el ISBN sea el proporcionado por el usuario en la tabla principal.
        Creamos un boton de actualizar que nos envia a esa funcion al ser presionado.'''
        
        try:
            connection=sqlite3.connect('Hemeroteca.db')
            c=connection.cursor()
            c.execute('PRAGMA foreign_keys=ON')
            c.execute('SELECT * FROM Libros WHERE ISBN='+self.e_selection.get())
            records=c.fetchall()

            
            self.editor=Toplevel()
            self.editor.title('ACTUALIZAR DATOS DEL LIBRO:')
            self.editor.geometry('500x400+550+20')
            self.editor.configure(bg='light slate grey')

           
            self.e_l_gnral=Label(self.editor, text='FORMULARIO CON DATOS DE LIBROS:').grid(row=0, column=0,columnspan=3, padx=5, pady=5)
            self.e_e_ISBN=Entry(self.editor,  width=55)
            self.e_e_ISBN.grid(row=1, column=1, columnspan=2)
            self.e_l_ISBN=Label(self.editor, text='ISBN sin guiones: ',bg='light slate grey',fg='white').grid(row=1, column=0,padx=5, pady=5 )
            self.e_e_title=Entry(self.editor, width=55)
            self.e_e_title.grid(row=2, column=1, columnspan=2)
            self.e_l_title=Label(self.editor, text='Titulo:',bg='light slate grey',fg='white').grid(row=2, column=0,padx=5, pady=5)
            self.e_l_genre=Label(self.editor, text='Genero:',bg='light slate grey',fg='white').grid(row=3, column=0,padx=5, pady=5)
            self.editor_e_genre=Entry (self.editor, width=30)
            self.editor_e_genre.grid(row=3, column=2, columnspan=2)
            self.editor_rb_genre1= Radiobutton(self.editor, text='Accion', variable=self.editor_genre, value='Accion', command=self.new_chose).grid(row=4,column=0,  padx=5, pady=5)
            self.editor_rb_genre2= Radiobutton(self.editor, text='Horror', variable=self.editor_genre,value='Horror', command=self.new_chose).grid(row=4,column=1,  padx=5, pady=5)
            self.editor_rb_genre3= Radiobutton(self.editor, text='Ciencia Ficcion', variable=self.editor_genre,value='Ciencia Ficcion', command=self.new_chose).grid(row=4,column=2,  padx=5, pady=5)
            self.editor_rb_genre4= Radiobutton(self.editor, text='Romantica', variable=self.editor_genre, value='Romantica', command=self.new_chose).grid(row=5,column=0,  padx=5, pady=5)
            self.editor_rb_genre5= Radiobutton(self.editor, text='Comedia', variable=self.editor_genre, value='Comedia', command=self.new_chose).grid(row=5,column=1,  padx=5, pady=5)
            self.editor_rb_genre6= Radiobutton(self.editor, text='Drama', variable=self.editor_genre,value='Drama', command=self.new_chose).grid(row=5,column=2, padx=5, pady=5)

            
            self.e_e_author=Entry(self.editor, width=55)
            self.e_e_author.grid(row=6, column=1,columnspan=2 )
            self.e_l_author=Label(self.editor, text='Autor: ',bg='light slate grey',fg='white').grid(row=6, column=0,padx=5, pady=5)
            self.e_l_sinopsis=Label(self.editor, text='Sinopsis: ',bg='light slate grey',fg='white').grid(row=7, column=0,padx=5, pady=5)
            self.e_e_sinopsis= Text(self.editor, width=45, height=5)
            self.e_e_sinopsis.grid(row=7, column=1, columnspan=3, padx=5, pady=5 )

            for record in records:
                self.e_e_ISBN.insert(0,record[0])
                self.e_e_title.insert(0, record[1])
                self.editor_e_genre.insert(0, record[2])
                self.e_e_author.insert(0,record[3])
                self.e_e_sinopsis.insert(1.0, record[4])

                
            self.b_update=Button(self.editor, text='Actualizar datos', command=self.update, bd=5).grid(row=9, column=0, columnspan=3,padx=5, pady=5)

            connection.commit()
        
        except Exception as Expt:
            showwarning (title='ATENCION',message='Da "Consultar datos" y selecciona un libro existente en "Elegir ISBN", antes de presionar "Actualizar datos".')
        
root=Tk()
Books(root)
root.mainloop()
