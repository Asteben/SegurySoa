import socket
import sys
import mysql.connector
import json


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('127.0.0.1', 5000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Conexion base de datos
db = mysql.connector.connect(user="root",password="root123",host="localhost",database="mydb1")
c = db.cursor()

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
            print('received {!r}'.format(aux))

            datos = eval(aux)
            print(datos)
            sql1 = "SELECT Monto, Fecha, Numero_cuenta_origen, Comentario FROM TransaccionRecivida WHERE Cuenta_idCuenta = (%s)"
            c.execute(sql1,(datos["idCuenta"],))
            rows = c.fetchall()
            print(rows)
            db.commit()

            aux = 0
            while aux < len(rows):
                if rows[aux][3] == None:
                    rows[aux] = list (rows[aux])
                    rows[aux][3] = "sin comentario"
                    rows[aux] = tuple (rows[aux])
                aux = aux + 1

            jrows = json.dumps(rows,default=str)
            brows = b'' + jrows

            connection.sendall(brows)
            break
        a = 1
        c.close()
        connection.close()
    finally:
        # Clean up the connection
        connection.close()
db.close()
