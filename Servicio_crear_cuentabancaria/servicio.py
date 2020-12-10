import socket
import sys
import sqlite3


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('127.0.0.1', 5000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Conexion base de datos
conn = sqlite3.connect('banco.sqlite')
cur = conn.cursor()

a = 0 
while a == 0:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        while True:
            aux = connection.recv(250)
            #print('received {!r}'.format(aux))

            datos = eval(aux)
            #print(datos)


            #se verifica si existe un usuario con ese nombre de usuario
            sql = "SELECT Usuario_idUsuario FROM Cuenta WHERE Numero = %s;"
            data_search = (datos['Numero'])
            cur.execute(sql, data_search)
            myresult = cur.fetchall()
            print("Si existe una cuenta con este número aparecerá a continuación:",myresult)
            conn.commit()
            
            if len(myresult): #si ya existe la cuenta
                print("Error")
                connection.sendall(b'False')
            
            else: #si no existe la cuenta
                sql = "INSERT INTO Cuenta (Numero, Saldo, Usuario_idUsuario, Tipo_idTipo) VALUES (%s, 0, %s, %s)"
                datainsert = (datos['Numero'], datos['Usuario_idUsuario'],datos['Tipo_idTipo'])
                cur.execute(sql,datainsert)
                conn.commit()
                connection.sendall(b'True')
                
            break
        connection.close()
        a = 1

    finally:
        # Clean up the connection
        connection.close()