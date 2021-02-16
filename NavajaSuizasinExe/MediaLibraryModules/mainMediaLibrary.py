from tkinter import *


class MainMediaLibrary():
    def __init__(self, LibraryWindow):
        self.LibraryWindow= LibraryWindow
        LibraryWindow.title('BIENVENIDO A LA HEMEROTECA')
        LibraryWindow.geometry ('370x300')
        LibraryWindow.config(bg='light slate grey')
           

        self.Customer_button=Button (LibraryWindow, text='CLIENTES',bd=5,command=self.accessCustomers).place(x=75, y=40)
        self.Book_button= Button (LibraryWindow, text='LIBROS', bd=5, command=self.accessBooks).place(x=75,y=80)
        self.Film_button= Button (LibraryWindow,text='PELICULAS', bd=5, command=self.accessFilms).place (x=75, y=120)
        self.Book_preferences_button= Button (LibraryWindow, text='LIBROS PREFERIDOS', bd=5, command=self.accessBookPreferences).place (x=75, y=160)
        self.Films_preferences_button= Button (LibraryWindow, text='PELICULAS PREFERIDAS', bd=5, command= self.accessFilmPreferences).place (x=75, y=200)

    def accessBooks(self):
       
        from MediaLibraryModules import Books

    def accessFilms(self):
       
        from MediaLibraryModules import Films
        
    def accessCustomers(self):
       
        from MediaLibraryModules import Customers

    def accessFilmPreferences(self):

        from MediaLibraryModules import SeenFilms

    def accessBookPreferences(self):

        from MediaLibraryModules import ReadBooks

root=Toplevel()
MainMediaLibrary(root)
root.mainloop()
