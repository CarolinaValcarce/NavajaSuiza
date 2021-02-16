from tkinter import *
from tkcalendar import Calendar
import sqlite3
from tkinter.messagebox import showerror,showwarning
from datetime import date, datetime

class ReadBooks():
    def __init__(self, master):

        '''Creamos un layout general formado por etiquetas, campos de entrada, radiobutton, calendario (que por defecto especifica la fecha de hoy) y 3 botones.
        Uno para confirmar la fecha introducida en el calendario y los otros dos: guardar registro y mostrar registros.'''
        
        self.master=master
        master.title('LIBROS LEIDOS DE LA HEMEROTECA:')
        master.geometry('550x525+500+0')
        master.configure(bg='light slate grey')
        self.score=IntVar()

             
        self.l_customer=Label(master,text='Introduce DNI de CLIENTE:',bg='light slate grey', fg='white').place (x=50, y=40)
        self.e_customer=Entry(master,width=20) 
        self.e_customer.place(x=350, y=40)
        self.l_book= Label (master,text='Introduce ISBN del Libro:',bg='light slate grey', fg='white').place(x=50, y=80)
        self.e_book= Entry (master, width=20)
        self.e_book.place(x=350, y=80)
        self.l_score= Label (master,text='Puntuacion sobre 10 que da el cliente a la pelicula:',bg='light slate grey', fg='white').place(x=50, y=120)
        self.l_score2=Label (master,text='(Clica un boton del 1 al 10)',bg='light slate grey',fg='white',font=('Verdana',7)).place (x=50,y=135)
        self.e_score= Entry (master,width=20)
        self.e_score.place(x=350, y=120)
        for i in range(1,11):
            self.rb_score= Radiobutton(master, text=''+str(i),value=i,variable=self.score, command=self.get_score).place(x=(40+35*i),y=160)

        self.calendar= Calendar(master,selectmode='day', year=date.today().year, month=date.today().month, day=date.today().day)
        self.calendar.place (x=250, y=200)

        self.b_selectiondate=Button(master,text='Confirma fecha de lectura',bd=5,command=self.write_date).place (x=50,y=250)

        self.b_save= Button (master, text='Guardar datos',bd=5,command=self.save).place(x=50,y=350)
        self.b_show= Button (master, text='Mostrar datos', bd=5, command=self.show).place (x=350, y=400)


    def save(self):

        ''' Creamos la conexion con la bbdd. Creamos una tabla donde la clave primaria es compuesta y esta formada por 2 ajenas una de cada tabla:
        libros y clientes. Debemos activar las claves ajenas con PRAGMA no solo en la tabla hija sino en cada una de las conexiones de las tablas padre.
        Restringimos las claves foraneas a la modificacion o eliminacion en casacada desde las tablas padre.
        Recogemos los valores del registro introducido por el usuario y los introducimos en la tabla siempre que la fecha no sea posterior al dia de hoy.
        Borramos los campos de entrada creados por el usuario.
        Creamos una excepcion si las claves ajenas (DNI y ISBN) introducidas por el usuario, no existen. O si esas claves ajenas,
        que es la primaria de esta tabla, ya han sido introducidas (mismo libro y mismo cliente).
        '''
        try:
            c=sqlite3.connect('Hemeroteca.db')
            cursor=c.cursor()
            cursor.execute('PRAGMA foreign_keys=ON')
            #cursor.execute ('DROP TABLE LibrosLeidos')
            cursor.execute('''CREATE TABLE IF NOT EXISTS LibrosLeidos (DNI_Cliente INTEGER,
                ISBN_Libro INTEGER , Puntuacion INTEGER, Fecha TEXT,
                PRIMARY KEY(DNI_Cliente, ISBN_Libro),
                FOREIGN KEY (DNI_Cliente) REFERENCES Clientes(DNI) ON UPDATE CASCADE ON DELETE CASCADE ,
                FOREIGN KEY(ISBN_Libro) REFERENCES Libros(ISBN) ON UPDATE CASCADE ON DELETE CASCADE)''')

            if ((datetime.strptime(self.calendar.get_date(),'%m/%d/%y').date())<=date.today()):   
            
                cursor.execute ('''INSERT INTO LibrosLeidos ( DNI_Cliente,
                            ISBN_Libro, Puntuacion, Fecha) VALUES (?,?,?,?)''',
                           (self.e_customer.get(),self.e_book.get(), self.score.get(), self.calendar.get_date()))

                self.e_customer.delete(0,END)
                self.e_book.delete(0,END)
                self.e_score.delete(0,END)
                self.calendar_label= Label(self.master,text='                  ',bg='light slate grey', fg='white').place(x=100,y=300)
              
                c.commit()
                c.close()
            else:
                showwarning(title='CUIDADO!', message='Debes introducir una fecha anterior a hoy o hoy')
            
        except Exception as excep:
            showerror(title='SE HA PRODUCIDO UN  ERROR', message='Ese cliente con ese mismo libro ya existen. '+'\n'+
            'O bien, estas introduciendo un cliente o un libro inexistentes')

    def show(self):

        '''Volvemos a crear la conexion. Seleccionamos todos los registros de la tabla creada y
        les recogemos en una etiqueta separados por salto de linea. Recogemos la excepcion si la tabla esta todavia vacia. '''
        try:
            connection=sqlite3.connect('Hemeroteca.db')
            cursor=connection.cursor()
            cursor.execute('PRAGMA foreign_keys=ON')
            cursor.execute ('SELECT * FROM LibrosLeidos')
            records=cursor.fetchall()
            print(records)
            print_records=''

            for record in records:
                print_records+= str(record)+'\n'

            self.records_label= Label (self.master,text=print_records,font=('Helvetica',10),bg='light slate grey', fg='white').place(x=50, y=400)

            connection.commit()
            connection.close()
        except Exception as warning:
            showwarning(title='ATENCION', message='Todavia no has introducido la preferencia de ningun cliente por ningun libro')

    def get_score(self):
        
        '''Rellenamos el campo de entrada de puntuacion automaticamente con la seleccion de puntuacion presionando el radiobutton por el usuario.'''
        self.e_score.delete(0,END)
        self.e_score.insert(0,self.score.get())
   
    def write_date(self):

        '''Creamos una etiqueta que recoja la fecha escrita seleccionada por el usuario al pulsar en el calendario.  '''
        self.calendar_label= Label(self.master,text= self.calendar.get_date()+'   ',bg='light slate grey', fg='white').place(x=100,y=300)


root=Toplevel()
ReadBooks(root)
root.mainloop()
