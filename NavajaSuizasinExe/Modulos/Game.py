from tkinter import*
import random
from tkinter.messagebox import showwarning

class Game():

    
    def __init__(self, root):


        self.root=root
        self.root.title('Juego del Ahorcado')
        
        '''Creamos una ventana a la derecha y abajo de la principal,
        con un campo de insercion de la letre y dos etiquetas con las instrucciones del juego.
        Creamos un boton de confirmar para cuando el usuario introduzca la letra.
        Y varias etiquetas con tantos _ como letras tiene la palabra separados po un x+30.'''
        
        self.root.geometry('480x260+650+50')
        self.root.config(bg='light slate grey')

        self.entryletter= Entry (self.root,width=5,font=('Verdana',10))
        self.entryletter.place (x=175, y=100)
        self.introduction= Label(self.root, text='BIENVENIDO al JUEGO DEL AHORCADO', font=('Verdana',15)).place(x=10, y=20)
        self.instruction= Label (self.root, text=' Comienza a adivinar... Sustantivo en singular.',font=('Verdana',10)).place (x=7, y=60)
        self.instruction2= Label (self.root, text='Introduce una letra:').place (x=25, y=100)


        self.click_button=Button(self.root,text='Confirma',font=('Verdana',10),bd=5,command=self.check).place (x=300, y=97)    

        self.guessWord= [Label (self.root,text='_', font=('Verdana', 20)) for _ in word]
        initialX=100
        for i in range(len(word)):
            self.guessWord[i].place(x=initialX, y=200)
            initialX+=30


    '''Con la funcion check creamos la logica del juego. Fuera de la funcion inicializamos las vidas a 7 y las letras acertadas a 0.
    Asi cada vez que controle una letra entrando en la funcion, esa vidas y letras acertadas cambiaran, hacemos para ello la variable global.
    Creamos un condicional de que si la letra esta en la palabra mas de una vez, incorpore cuantas veces a la variable guessletters y en la etiqueta
    de la palabra a adivinar si la letra corresponde con las de las de la palabra, incorporarla.
    Si la letra solo esta una vez, marcarla en la etiqueta e incrementar la variable guessletters en 1.
    Ademas mostrar mensaje en el caso de que el numero de letras acertadas corresponda con la longitud de la palabra.
    Y vaciar el campo de entrada de la letra tras incorporarla a la etiqueta.
    Y si la letra no esta en la palabra, perder una vida. Y mostrar mensaje dependiendo de cuantas vidas queden.'''

    
    def check(self):

        usedLetters=[]
        usedLetters.append ((self.entryletter.get()).lower())
        print (usedLetters)
       
        global guessLetters
        global lifes
        global word
         
       
        if(self.entryletter.get()).lower() in word:
            if word.count((self.entryletter.get()).lower())>1:
                guessLetters= guessLetters + word.count((self.entryletter.get()).lower())
                for i in range (0,len(word)):
                    if word[i]== (self.entryletter.get()).lower():
                        self.guessWord[i].config(text=''+ (self.entryletter.get()).lower())
                self.entryletter.delete(0,END)
                
            else:
                self.guessWord[word.index((self.entryletter.get()).lower())].config(text=''+ (self.entryletter.get()).lower())
                guessLetters=guessLetters+1
                self.entryletter.delete(0,END)
                
            if guessLetters==len(word):
                showwarning(title='ENHORABUENA!!!', message='Has acertado la palabra.')
                self.root.destroy()

           
        else:
            lifes=lifes-1
            if lifes>1:
                showwarning(title='ATENCION!!',message='Te quedan '+str(lifes)+' vidas.')
                self.entryletter.delete(0,END)
            else:
                if lifes==1:
                    showwarning (title='ATENCION!!',message='Te queda 1 vida. Ultima')
                    self.entryletter.delete (0,END)
                if lifes==0:
                    showwarning (title='PERDISTE' , message='No tienes mas vidas!!!.  '
                             'La palabra era: '+word.upper())
                    self.root.destroy()

lifes=7
guessLetters=0

words_group=('drogadicto','antenista','milagro','conflicto','hechicero','sabiduria','mazapan','mensaje','holograma','educacion','eucaristia','dialogo','pastor',
             'saludo','barbaro','ratero', 'especimen', 'mercado','abadesa', 'caballo', 'fabrica','fachada','habitat', 'habitud','iceberg','macarra', 'objeto',
             'quedada','quejica','rabanal','sablazo','taberna','vacante','edicion','egoismo','ejemplo','abdomen','absenta','acetona','zancudo','tutoria','urologo',
            'tributo','tulipan', 'tumbona','tomador','topacio', 'tropico','terraza','surtido','taladro', 'bebida','comida','diamante','equipaje','meteorito',
             'caramelo','sabana','tejido','hospital','universidad', 'escuela','arbitro','adolescencia','tumba','adivinanza','pastel','espiritu', 'flamenco', 'victoria')
word=random.choice(words_group)

root=Tk()
Game(root)
root.mainloop()




