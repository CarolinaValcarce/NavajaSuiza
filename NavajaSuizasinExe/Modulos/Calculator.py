from tkinter import*

class Calculator:

    def __init__(self, master):

        '''Colocamos la ventana con la calculadora de cierto tamano y a la derecha y abajo(+500+70) de la ventana de la interfaz principal.'''
        self.master=master
        master.title('Calculadora')
        master.geometry('370x400+600+70')
        master.config(bg='light slate grey')

        '''Tenemos un grid tipo tabla. Hacemos cada una de las columnas y filas expandibles en posicion. Por si se maximiza la ventana.'''
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.rowconfigure(1, weight=1)
        master.columnconfigure(2, weight=1)
        master.rowconfigure(2, weight=1)
        master.rowconfigure(3, weight=1)
        master.rowconfigure(4, weight=1)
        master.rowconfigure(5, weight=1)

        '''Creamos una pantalla para insertar los numeros con tamano grande de letra y le damos la amplitud de las 3 columnas de la tabla.'''
        self.screen=Entry (master,width=50, font=('Verdana',25))
        self.screen.grid(row=0,column=0,pady=2, padx=2, columnspan=3, ipadx=35,ipady=20)

            
        '''Creamos todos los botones del grid con su correspondiente command, y los posicionamos en filas y columnas.
        Usamos el lambda para que un mismo metodo funcione igual con independencia de la tecla pulsada del 0 al 9.
        A la tecla BORRAR le damos una amplitud de las 3 columnas.'''
        self.button0=Button (master,text='0',font=('Verdana',18),bd=5, command=lambda:self.clicar(0)).grid (row=4, column=1,pady=2, padx=2, ipadx=35,ipady=20)
        self.button1=Button (master,text='1',font=('Verdana',18),bd=5, command=lambda:self.clicar(1)).grid (row=3, column=0,pady=2, padx=2, ipadx=35,ipady=20 )
        self.button2=Button (master,text='2',font=('Verdana',18),bd=5, command=lambda:self.clicar(2)).grid (row=3, column=1,pady=2, padx=2,ipadx=35,ipady=20 )
        self.button3=Button (master,text='3',font=('Verdana',18),bd=5, command=lambda:self.clicar(3)).grid (row=3, column=2,pady=2, padx=2,ipadx=35,ipady=20 )   
        self.button4=Button (master,text='4',font=('Verdana',18),bd=5, command=lambda:self.clicar(4)).grid (row=2, column=0,pady=2, padx=2,ipadx=35,ipady=20 )
        self.button5=Button (master,text='5',font=('Verdana',18),bd=5, command=lambda:self.clicar(5)).grid (row=2, column=1,pady=2, padx=2,ipadx=35,ipady=20 )
        self.button6=Button (master,text='6',font=('Verdana',18),bd=5, command=lambda:self.clicar(6)).grid (row=2, column=2,pady=2, padx=2,ipadx=35,ipady=20 )
        self.button7=Button (master,text='7',font=('Verdana',18),bd=5, command=lambda:self.clicar(7)).grid (row=1, column=0,pady=2, padx=2,ipadx=35,ipady=20)
        self.button8=Button (master,text='8',font=('Verdana',18),bd=5, command=lambda:self.clicar(8)).grid (row=1, column=1,pady=2, padx=2,ipadx=35,ipady=20)
        self.button9=Button (master,text='9',font=('Verdana',18),bd=5, command=lambda:self.clicar(9)).grid (row=1, column=2,pady=2, padx=2,ipadx=35,ipady=20 )
        self.clear=Button (master,text='BORRAR',font=('Verdana',18),bd=5, command= self.cancel).grid (row=6, column=0,columnspan=3, pady=2, padx=2, ipadx=80,ipady=20 ) 
        self.plus=Button (master,text='+',font=('Verdana',18),bd=5, command= self.add ).grid (row=4, column=0,pady=2, padx=2,ipadx=34,ipady=20 )
        self.minus=Button (master,text='-',font=('Verdana',18),bd=5, command= self.subtract).grid (row=5, column=2,pady=2, padx=2, ipadx=38,ipady=20 )
        self.product=Button (master,text='*',font=('Verdana',18), bd=5, command= self.multiply).grid (row=5, column=1,pady=2, padx=2,ipadx=35,ipady=20 )
        self.between=Button (master,text='/',font=('Verdana',18),bd=5, command= self.division).grid (row=5, column=0,pady=2, padx=2,ipadx=38,ipady=20 )
        self.equal=Button (master,text='=',font=('Verdana',18),bd=5, command= self.is_equal).grid (row=4, column=2,pady=2, padx=2,ipadx=34,ipady=20 )



    '''Creamos las diferentes funciones tanto sumar, restar, multiplicar y dividir como el hecho de clicar y ver resultado en pantalla y borrar pantalla.'''
    def clicar(self,number):
        e=self.screen.get()  
        self.screen.delete (0,END)
        '''e representa un solo digito por tanto por cada click borramos la pantalla y ponemos los digitos ya escritos mas el ultimo.'''
        self.screen.insert(0,str(e)+str( number))
         
    def cancel(self):
        self.screen.delete(0,END)


    ''' En cada uno de los 4 metodos siguientes creamos variables globales para ser reconocidas dentro del metodo equal().
    En cada metodo reconoce el numero clicado anterior y borra pantalla.'''
    def add(self):
        global first_n, operation
        operation='add'
        first_n =self.screen.get()
        self.screen.delete(0,END)          

    def subtract(self):
        global first_n, operation
        operation='subtract'
        first_n =self.screen.get()
        self.screen.delete(0,END)

    def multiply(self):
        global first_n, operation
        operation='multiply'
        first_n =self.screen.get()
        self.screen.delete(0,END)

    def division(self):
        global first_n, operation
        operation='division'
        first_n =self.screen.get()
        self.screen.delete(0,END)

        
    '''En equal()  recoge el ultimo numero en pantalla antes de clicar igual,y borrar pantalla.
    Y dependiendo de si se pulso un mas, menos, por o igual se hace la operacion correspodiente con un condicional.
    Pasamos todo a float, ya que si realizamos operaciones continuas, nos interesa que reconozca el float generado de otra operacion anterior.
    Ademas recogemos los errores que se pueden generar si el primer o el segundo operando no se presionan antes del igual
    con 'Error' que aparece en pantalla. Y si se divide entre 0 que aparezca en pantalla Infinito.'''
    def is_equal(self):

        global equal_n,operation
        equal_n =self.screen.get()
        self.screen.delete(0,END)
        
        if operation=='add':
            if (str(first_n)=='' or str(equal_n)==''):
                self.screen.insert(0,'Error')
            else:
                self.screen.insert(0, float(first_n)+ float(equal_n))
                
        elif operation=='subtract':
            if (str(first_n)=='' or str(equal_n)==''):
                self.screen.insert(0,'Error')
            else:
                self.screen.insert(0, float(first_n)-float(equal_n))
                
        elif operation=='division':
            
            if (str(first_n)=='' or str(equal_n)==''):
                self.screen.insert(0,'Error')
            else:
                if int(equal_n)==0:
                    self.screen.insert(0, 'Infinito')
                else:
                    self.screen.insert(0, float(first_n)/ float(equal_n))
                    
        elif operation=='multiply':
            if (str(first_n)=='' or str(equal_n)==''):
                self.screen.insert(0,'Error')
            else:
                self.screen.insert(0, float(first_n)* float(equal_n))



r=Tk()
Calculator(r)
r.mainloop()
