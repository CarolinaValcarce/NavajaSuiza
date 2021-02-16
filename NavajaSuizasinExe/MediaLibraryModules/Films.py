from tkinter import*
from tkinter.messagebox import showwarning, showerror
import sqlite3

class Films():
    def __init__(self,r):

        '''Creamos el layout general, con etiquetas, radiobutton, campos de texto, y entrada multilinea y con 4 botones'''

        self.r=r
        r.title('PELICULAS DISPONIBLES EN LA HEMEROTECA')
        r.geometry('500x490+550+0')
        r.configure(bg='light slate grey')

        connection=sqlite3.connect('Hemeroteca.db')
        cursor=connection.cursor()

        
        self.genre=StringVar()

        self.l_gnral=Label(r, text='FORMULARIO CON DATOS DE PELICULAS:').grid(row=0, column=0,columnspan=3, padx=5, pady=5)
        self.e_code=Entry(r,  width=55)
        self.e_code.grid(row=1, column=1, columnspan=2)
        self.l_code=Label(r, text='Codigo de pelicula: ',bg='light slate grey',fg='white').grid(row=1, column=0,padx=5, pady=5 )
        self.e_title=Entry(r, width=55)
        self.e_title.grid(row=2, column=1, columnspan=2)
        self.l_title=Label(r, text='Titulo:',bg='light slate grey',fg='white').grid(row=2, column=0,padx=5, pady=5)
        self.l_genre=Label(r, text='Genero:',bg='light slate grey',fg='white').grid(row=3, column=0,padx=5, pady=5)
        self.rb_genre1= Radiobutton(r, text='Accion', variable=self.genre, value='Accion').grid(row=4,column=0,  padx=5, pady=5)
        self.rb_genre2= Radiobutton(r, text='Horror', variable=self.genre,value='Horror').grid(row=4,column=1,  padx=5, pady=5)
        self.rb_genre3= Radiobutton(r, text='Ciencia Ficcion', variable=self.genre,value='Ciencia Ficcion').grid(row=4,column=2,  padx=5, pady=5)
        self.rb_genre4= Radiobutton(r, text='Romantica', variable=self.genre, value='Romantica').grid(row=5,column=0,  padx=5, pady=5)
        self.rb_genre5= Radiobutton(r, text='Comedia', variable=self.genre, value='Comedia').grid(row=5,column=1,  padx=5, pady=5)
        self.rb_genre6= Radiobutton(r, text='Drama', variable=self.genre,value='Drama').grid(row=5,column=2, padx=5, pady=5)

        self.genre.get()

        self.e_director=Entry(r, width=55)
        self.e_director.grid(row=6, column=1,columnspan=2 )
        self.l_director=Label(r, text='Director: ',bg='light slate grey',fg='white').grid(row=6, column=0,padx=5, pady=5)
        self.l_sinopsis=Label(r, text='Sinopsis: ',bg='light slate grey',fg='white').grid(row=7, column=0,padx=5, pady=5)
        self.e_sinopsis=Text(r, width=45, height=5)
        self.e_sinopsis.grid(row=7, column=1, columnspan=3, padx=5, pady=5 )


        self.b_send= Button (r, text='Guardar datos', bd=5,command=self.save).grid(row=14, column=0, columnspan=2,padx=5, pady=5)
        self.b_query= Button (r, text='Consultar datos',bd=5, command=self.query).grid(row=15, column=0, columnspan=2,padx=5, pady=5)
        self.e_selection= Entry (r, width=20)
        self.e_selection.grid(row=13, column=1)
        self.l_selection=Label(r, text='Elegir codigo:',bg='light slate grey', fg='white').grid(row=13, column=0)
        self.b_delete=Button(r, text= 'Borrar datos', bd=5,command=self.delete).grid(row=14, column=2,padx=5, pady=5)
        self.b_edit=Button(r, text='Actualizar datos',bd=5, command=self.edit).grid(row=15, column=2, columnspan=1, padx=5, pady=5)
        self.records_label=Label(self.r)
        
        connection.close()

    def save(self):

        '''Creamos una conexion a Hemeroteca y creamos la tabla introduciendo los valores que nos proporciona en los capos rellenados el usuario.
        Vaciamos los campos de entrada de texto.
        Creamos una excepcionn si nos introduce los datos de una pelicula con un codigo de otra pelicula ya registrada.'''
        
        try:
            connection=sqlite3.connect('Hemeroteca.db')
            cursor=connection.cursor()
            #cursor.execute('DROP TABLE Peliculas')
            cursor.execute('PRAGMA foreign_keys=ON')
            cursor.execute ('''CREATE TABLE IF NOT EXISTS Peliculas
                            (Codigo INTEGER PRIMARY KEY, Titulo TEXT NOT NULL, Genero TEXT, Director TEXT, Sinopsis TEXT )''' )
            if (self.e_title.get()!=''):
                cursor.execute ('INSERT INTO Peliculas (Codigo, Titulo, Genero, Director, Sinopsis) VALUES (?,?,?,?,?)',
                            (self.e_code.get(),self.e_title.get(), self.genre.get(),self.e_director.get(),self.e_sinopsis.get(1.0,END)))
                self.e_code.delete(0,END)
                self.e_title.delete(0,END)
                self.genre.set('Accion')
                self.e_director.delete(0, END)
                self.e_sinopsis.delete(1.0,END)
                
                connection.commit()
            else:
                showerror(title='ATENCION', message='El titulo no puede estar vacio')

        except Exception as error:
            showerror(title='ATENCION', message='Ya existe una pelicula con ese codigo. Corrige el codigo erroneo antes.')

    def query(self):

        '''Creamos conexion con Hemeroteca. Selecccionamos todos los datos de los registros ya incorporados.
        Y los imprimimos en una etiqueta separados por salto de linea. Recogemos la excepcion si no hay todavia ningun registro.'''
        
        connection=sqlite3.connect('Hemeroteca.db')
        cursor= connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        
        try:
            cursor.execute('SELECT Codigo,Titulo,Genero,Director FROM Peliculas')
            records=cursor.fetchall()
            print(records)
            printrecords=''

            for record in records:
                printrecords+= str(record)+'\n'
            self.records_label.destroy()
            self.records_label= Label(self.r, text=printrecords)
            self.records_label.grid (row=16, column=0, columnspan=3)

            connection.commit()
        except Exception as e:
            showwarning(title='ATENCION', message='Todavia no hay ninguna pelicula disponible')
        

    def delete(self):

        '''Conectamos con Hemeroteca, borramos el regisro identificado por el codigo que nos proporciona el usuario.
        Recogemos el error si el codigo proporcionado es inexistente. Borramos el campo de entrada del codigo.'''
        
        connection=sqlite3.connect('Hemeroteca.db')
        cursor=connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        try:
            cursor.execute ('DELETE FROM Peliculas WHERE Codigo='+self.e_selection.get())
        except Exception as exc:
            showwarning(title='ATENCION!!!', message='Da "Consultar datos" y selecciona una pelicula existente en "Elegir codigo", antes de presionar "Borrar datos".')

        self.e_selection.delete(0,END)
        connection.commit()
     

    def update(self):

        '''Conectamos con Hemeroteca y actuaiizaos todos los valores del registro con los proporcionados en los campos de la ventana de edicion,
        del registro cuyo codigo sea el proporcionado por el usuario en el layout general.
        Borramos el campo de entrada del codigo. Cerramos la ventana de edicion. Creamos mensaje de aviso si nos crea un titulo vacio. '''
        
        connection=sqlite3.connect('Hemeroteca.db')
        cursor= connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        if (self.editor_e_title.get()!=''):
            cursor.execute ('UPDATE Peliculas SET Codigo=(?), Titulo=(?), Genero=(?), Director=(?), Sinopsis=(?) WHERE Codigo=(?)',
                        (self.editor_e_code.get(), self.editor_e_title.get(), self.editor_e_genre.get(), self.editor_e_director.get(), self.editor_e_sinopsis.get(1.0,END), self.e_selection.get()))
            self.e_selection.delete(0,END)
            connection.commit()
            self.editor.destroy()    

        else:
            showwarning(title='ATENCION', message='El campo titulo no puede estar vacio.')


    def new_chose(self):

        '''Rellenamos el campo de entrada del genero en la ventana de edicion con la opcion seleccionada con el radiobutton por el usuario.'''
        self.editor_e_genre.delete(0,END)
        self.editor_e_genre.insert(0,self.editor_genre.get())

    def edit(self):
        
        global editor
        global editor_e_code
        global editor_e_title
        global editor_genre
        self.editor_genre=StringVar()
        global editor_e_genre
        global editor_e_director
        global editor_e_sinopsis

        '''Conectamos con Hemeroteca.db, seleccionamos el registro donde el codigo sea el introducido por el usuario en el layout general.
        Creamos una ventana de edicion y rellenamos los campos de texto con los valores de ese registro.
        Creamos un boton de actualizar que nos redirecciona a la . Recogemos la excepcion si nos da un codigo inexistente en el layout general.'''
        
        try: 
            connection=sqlite3.connect('Hemeroteca.db')
            cursor=connection.cursor()
            cursor.execute('PRAGMA foreign_keys=ON')
            cursor.execute ('SELECT * FROM Peliculas WHERE Codigo='+self.e_selection.get())
            records=cursor.fetchall()

            self.editor=Toplevel()
            self.editor.title('ACTUALIZAR DATOS DE LA PELICULA:')
            self.editor.geometry('500x400+550+20')
            self.editor.configure(bg='light slate grey')

            self.editor_l_gnral=Label(self.editor, text='FORMULARIO CON DATOS DE PELICULAS:').grid(row=0, column=0,columnspan=3, padx=5, pady=5)
            self.editor_e_code=Entry(self.editor,  width=55)
            self.editor_e_code.grid(row=1, column=1, columnspan=2)
            self.editor_l_code=Label(self.editor, text='Codigo de pelicula: ',bg='light slate grey',fg='white').grid(row=1, column=0,padx=5, pady=5 )
            self.editor_e_title=Entry(self.editor, width=55)
            self.editor_e_title.grid(row=2, column=1, columnspan=2)
            self.editor_l_title=Label(self.editor, text='Titulo:',bg='light slate grey',fg='white').grid(row=2, column=0,padx=5, pady=5)
            self.editor_l_genre=Label(self.editor, text='Genero:',bg='light slate grey',fg='white').grid(row=3, column=0,padx=5, pady=5)
            self.editor_e_genre= Entry (self.editor, width=55)
            self.editor_e_genre.grid(row=3, column=1, columnspan=2)                       
            self.editor_rb_genre1= Radiobutton(self.editor, text='Accion', variable=self.editor_genre, value='Accion', command=self.new_chose).grid(row=4,column=0,  padx=5, pady=5)
            self.editor_rb_genre2= Radiobutton(self.editor, text='Horror', variable=self.editor_genre,value='Horror', command=self.new_chose).grid(row=4,column=1,  padx=5, pady=5)
            self.editor_rb_genre3= Radiobutton(self.editor, text='Ciencia Ficcion', variable=self.editor_genre,value='Ciencia Ficcion', command=self.new_chose).grid(row=4,column=2,  padx=5, pady=5)
            self.editor_rb_genre4= Radiobutton(self.editor, text='Romantica', variable=self.editor_genre, value='Romantica', command=self.new_chose).grid(row=5,column=0,  padx=5, pady=5)
            self.editor_rb_genre5= Radiobutton(self.editor, text='Comedia', variable=self.editor_genre, value='Comedia', command=self.new_chose).grid(row=5,column=1,  padx=5, pady=5)
            self.editor_rb_genre6= Radiobutton(self.editor, text='Drama', variable=self.editor_genre,value='Drama', command=self.new_chose).grid(row=5,column=2, padx=5, pady=5)

            self.editor_e_director=Entry(self.editor, width=55)
            self.editor_e_director.grid(row=6, column=1,columnspan=2)
            self.editor_l_director=Label(self.editor, text='Director: ',bg='light slate grey',fg='white').grid(row=6, column=0,padx=5, pady=5)
            self.editor_l_sinopsis=Label(self.editor, text='Sinopsis: ',bg='light slate grey',fg='white').grid(row=7, column=0,padx=5, pady=5)
            self.editor_e_sinopsis= Text(self.editor, width=45, height=5)
            self.editor_e_sinopsis.grid(row=7, column=1, columnspan=3, padx=5, pady=5)
             
            for record in records:
                self.editor_e_code.insert(0,record[0])
                self.editor_e_title.insert(0,record[1])
                self.editor_e_genre.insert(0,record[2])
                self.editor_e_director.insert (0,record[3])
                self.editor_e_sinopsis.insert (1.0,record[4])

            self.b_update=Button(self.editor, text='Actualizar datos', command=self.update, bd=5).grid(row=9, column=0, columnspan=3,padx=5, pady=5)
             
            connection.commit()

        except Exception as ex:
            showwarning (title='ATENCION',message='Da "Consultar datos" y selecciona una pelicula existente en "Elegir codigo", antes de presionar "Actualizar datos".')
       
root=Tk()
Films(root)
root.mainloop()
