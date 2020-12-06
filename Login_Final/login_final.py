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


            #********* Consulta BDD **********
            data_search = (datos['Email'],datos['Password'])
            cur.execute('SELECT * FROM usuario  WHERE Usuario.Email = ?AND Usuario.Password = ? ',data_search)
            myresult = cur.fetchall()
            print("DATOS ENCONTRADOS:",myresult)
            conn.commit()
            #********************


            if len(myresult): #si hay algo en el select, entonces existe la cuenta
                print("Logeado")
                connection.sendall(b'True')
            else:
                print("Error")
                connection.sendall(b'False')
            break

        a = 1
        connection.close()

    finally:
        connection.close()