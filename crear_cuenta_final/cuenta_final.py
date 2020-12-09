import socket
import sys
import sqlite3

#####CONEXION#######
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 5000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
sock.listen(1)
####################

##### Conexion base de datos #####
conn = sqlite3.connect('banco.sqlite')
cur = conn.cursor()
####################

a = 0 #Esto es basicamente hacer el stop al while.
while a == 0:

    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        while True:
            aux = connection.recv(250)
            datos = eval(aux) #Datos recibidos"
            print("DATOS RECIBIDOS DEL CLIENTE:",datos)


            #********* Crear usuario BDD **********
            data_search = (datos['Nombre'],datos['Email'],datos['Password'],datos['RUT'],datos['Edad'],datos['Telefono'])
            cur.execute('INSERT INTO Usuario (Nombre, Email, Password, Rut, Edad, Telefono) VALUES (?, ?, ?, ?, ?, ?)',data_search)
            conn.commit()
            
            #cur.execute('SELECT * FROM usuario') #Esto solo sirve para mostrar todos los usuarios de la bdd
            #myresult = cur.fetchall()
            #print("DATOS ENCONTRADOS:",myresult)
            #conn.commit()
            #********************

            connection.sendall(b'True')

            break

        a = 1
        connection.close()

    finally:
        connection.close()