import socket
import sys
import mysql.connector


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
while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        data = b''
        while True:
            aux = connection.recv(16)
            data= data + aux
            print('received {!r}'.format(aux))
            connection.sendall(aux)
            if aux == b'' :
                print('no data from', client_address)
                dataobject = eval(data)
                sql = "INSERT INTO usuario (Nombre, Email, Password, RUT, Edad, Telefono) VALUES ( %s, %s, %s, %s, %s, %s )"
                datainsert = (dataobject["Nombre"], dataobject["Password"], dataobject["Email"], dataobject["RUT"], dataobject["Edad"], dataobject["Telefono"])
                c.execute(sql, datainsert)
                db.commit()
                print(dataobject)
                break

    finally:
        # Clean up the connection
        connection.close()

c.close()
db.close()