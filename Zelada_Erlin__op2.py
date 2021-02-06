from tkinter import PhotoImage, Tk, Frame, Entry, Label, Button, W, E, Listbox, END
import psycopg2


class Fr_banco(Frame):

    def __init__(self, master):
        super().__init__(master, width=20, height=770)
        
        self.master = master
        self.pack()
        self.interface()
        self.mostrar_cliente()
        
         
    def iniciar (self):
        self.conn = psycopg2.connect(dbname="postgres", user="postgres", password="12345678", host="localhost", port="5432")
        self.cursor = self.conn.cursor()
        return self.cursor, self.conn
    def cerrar (self):
        self.conn.commit()
        self.conn.close()

    def ingresar_cliente(self,nombre, codigo, monto,estado):
        self.iniciar()
        self.sql = ''' INSERT INTO clientes(nombre, codigo, monto, estado) VALUES (%s, %s, %s, %s)'''
        self.cursor.execute(self.sql, (nombre, codigo, monto, estado))
        self.cerrar()
        self.mostrar_cliente()

    def mostrar_cliente(self):
        self.iniciar()
        self.cursor.execute(''' SELECT * FROM clientes''')
        row = self.cursor.fetchall()
        self.listbox = Listbox(self, width=20, height=10)
        self.listbox.grid(row=10, columnspan=2, sticky=W+E)
        for i in row:
            self.listbox.insert(END, i)
        self.cerrar()

    def borrar_cliente(self,codigo):
        self.iniciar()
        self.cursor.execute('''DELETE FROM clientes WHERE codigo = {0}'''.format(codigo))
        #self.row = self.cursor.fetchone()
        #self.mostrar_resultados(self.row)
        print("borrado")
        self.cerrar()
        self.mostrar_cliente()
        self.buscar(codigo)
    
    def cambiar_estado(self,codigo,estado):
        self.iniciar()
        self.sql = '''UPDATE clientes SET estado = %s where codigo = %s'''
        self.cursor.execute(self.sql, (estado,codigo))
        self.cerrar()
        self.mostrar_cliente()
        self.buscar(codigo)
        self.mostrar_cliente()
    

    def buscar(self,codigo):
        self.iniciar()
        self.cursor.execute(''' SELECT * FROM clientes WHERE codigo = {0}'''.format(codigo))
        self.row = self.cursor.fetchone()
        self.mostrar_resultados(self.row)
        self.cerrar()

    def mostrar_resultados(self, row):
        self.listbox = Listbox(self, width=20, height=1)
        self.listbox.grid(row=2, column=4, sticky=E+W)
        self.listbox.insert(END, row)

    def interface(self):
        
        self.label = Label(self, text='AÑADIR UN NUEVO CLIENTE')
        self.label.grid(row=0, column=1)
        
        # Ingresa Nombre de la persona
        self.label = Label(self, text="USUARIO")
        self.label.grid(row=1, column=0)

        self.entry_nombre = Entry(self)
        self.entry_nombre.grid(row=1, column=1)

        # Ingresar DNI de la persona
        self.label = Label(self, text="DNI")
        self.label.grid(row=2, column=0)

        self.entry_codigo = Entry(self)
        self.entry_codigo.grid(row=2, column=1)

        # Para ingresar monto de credito
        self.label = Label(self, text="MONTO")
        self.label.grid(row=3, column=0)

        self.entry_monto = Entry(self)
        self.entry_monto.grid(row=3, column=1)
        
        
        # Para ingresar estado de credito
        self.label = Label(self, text="ESTADO")
        self.label.grid(row=4, column=0)

        self.entry_estado = Entry(self)
        self.entry_estado.grid(row=4, column=1)


        #Boton para registrar
        self.button = Button(self, text="REGISTRAR",
                             command=lambda: self.ingresar_cliente(
                                self.entry_nombre.get(),
                                self.entry_codigo.get(),
                                self.entry_monto.get(),
                                self.entry_estado.get()
        ))
 
        self.button.grid(row=6, column=1, sticky=W+E)
        

        
        #Registro Visual
        self.label = Label(self, text="Registro")
        self.label.grid(row=9, columnspan=2, sticky=W+E)


        #Buscar por DNI == codigo
        self.label = Label(self, text="Buscar segun DNI")
        self.label.grid(row=0, column=4)

        self.codigo_buscar = Entry(self)
        self.codigo_buscar.grid(row=1, column=4)

        self.button = Button(self,text="BUSCAR",
                             command=lambda: self.buscar(
                                 self.codigo_buscar.get()
                                 ))
        self.button.grid(row=1, column=6)
        
        
        #borrar por codigo == DNI
        self.label = Label(self, text="Borrar segun DNI")
        self.label.grid(row=4, column=4)

        self.codigo_borrar = Entry(self)
        self.codigo_borrar.grid(row=5, column=4)

        self.button = Button(self, text="BORRAR",
                             command=lambda: self.borrar_cliente(
                                 self.codigo_borrar.get()
                             ))
        self.button.grid(row=5, column=6)
        
        #Cambiar estado por codigo
        self.label1 = Label(self, text="Cambiar estado segun DNI                  ")
        self.label1.grid(row=7, columnspan=7, sticky=E)
        
        
        self.label2 = Label(self, text="Ingrese DNI")
        self.label2.grid(row=8, column=3)
        self.codigo_cambiar = Entry(self)
        self.codigo_cambiar.grid(row=8, column=4)

        
        self.label3 = Label(self, text="Ingrese ESTADO")
        self.label3.grid(row=9, column=3)
        self.estado_cambiar = Entry(self)
        self.estado_cambiar.grid(row=9, column=4)


        self.button = Button(self, text="Cambiar",
                             command=lambda: self.cambiar_estado(
                                 self.codigo_cambiar.get(),
                                 self.estado_cambiar.get()
                             ))
        self.button.grid(row=8, column=6)
      
      
      
root = Tk()
root.geometry("530x430")

root.wm_title("EZETABANK")
app = Fr_banco(root)
root.iconbitmap("logo.ico")
app.mainloop()
