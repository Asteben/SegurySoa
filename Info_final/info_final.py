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
            data_search = (datos['Rut'],)
            cur.execute('SELECT * FROM usuario  WHERE Usuario.Rut = ? ',data_search)
            myresult = cur.fetchall()
            conn.commit()
            #********************

            if len(myresult):
                print("Enviando datos")

                info = ""
                for i in myresult[0]:
                    info = info + str(i) +" "

                info = bytes(info, 'utf-8')
                connection.sendall(info)
            else:
                print("Error")
                connection.sendall(b'False')


            break

        a = 1
        connection.close()

    finally:
        connection.close()