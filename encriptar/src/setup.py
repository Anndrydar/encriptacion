#Importaciones de librerias
from cryptography.fernet import Fernet
from tkinter import Tk, Frame, Label, Entry, Button, W, E, Listbox, END
import psycopg2

root = Tk()
root.title("Cifrar y Descifrar")
root.geometry("2000x2000")
root.configure(bg='#3b8eed')



#Funcion agregar nueva frase junto a su cifrado
def save_frase(frase):
    key = Fernet.generate_key()
    objeto_cifrado = Fernet(key)
    cifrado = objeto_cifrado.encrypt(str.encode(frase))
    conn = psycopg2.connect(dbname="mensaje", user="postgres",
                            password="", host="localhost", port="5432")
    cursor = conn.cursor()
    query = '''INSERT INTO frase(cuerpo, cuerpo_cifrado) VALUES (%s, %s)'''
    cursor.execute(query, (frase,cifrado))
    print("Datos agregados exitosamente")
    conn.commit()
    conn.close()

#Funcion mostrar todas las keys existentes en la BD    
def mostrarAll():
    conn = psycopg2.connect(dbname="mensaje", user="postgres",
                            password="", host="localhost", port="5432")
    cursor = conn.cursor()
    query = '''SELECT id, cuerpo_cifrado FROM frase'''
    cursor.execute(query)
    registro = cursor.fetchall()

    listbox = Listbox(frame, width=250, height=5)
    listbox.grid(row=10, columnspan=4, sticky=W+E)
    for i in registro:
      listbox.insert(END, i)

    conn.commit()
    conn.close()

#Funcion para descifrar por id del mensaje encriptado
def descifrar(id):
      conn = psycopg2.connect(dbname="mensaje", user="postgres",
                            password="", host="localhost", port="5432")
      cursor = conn.cursor()

      query = '''SELECT cuerpo FROM frase where id=%s'''
      cursor.execute(query, (id))
      row = cursor.fetchone()

      listbox = Listbox(frame, width=20, height=1)
      listbox.grid(row=14, columnspan=4, sticky=W+E)
      listbox.insert(END, row)                      

      conn.commit()
      conn.close()  



#Marco principal
frame = Frame()
frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
frame.configure(bg='white')

#Etiquetas
label = Label(frame, text="Agrega una frase")
label.grid(row=0, column=1)

label = Label(frame, text="Descifra una key por su id")
label.grid(row=11, column=1)

#entradas de texto
frase = Entry(frame)
frase.grid(row=1, column=1)
frase.focus()

llave = Entry(frame)
llave.grid(row=12, column=1)

#Botones
button = Button(frame, text="Cifrar",bg = "silver" ,command=lambda: save_frase(
    frase.get()))
button.grid(row=4, column=1, sticky=W+E)

button = Button(frame, text="Mostrar keys",bg = "silver" ,command=lambda: mostrarAll())
button.grid(row=5, column=1, sticky=W+E)

button = Button(frame, text="Descifrar", bg = "silver",command=lambda: descifrar(llave.get()))
button.grid(row=13, column=1, sticky=W+E)


root.mainloop()