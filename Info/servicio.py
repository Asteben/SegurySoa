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
db = mysql.connector.connect(user="root",password="",host="localhost",database="mydb1")
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
            sql = "SELECT * FROM usuario WHERE usuario.Rut = %s ;"
            data_search = (datos['Rut'],)
            c.execute(sql, data_search)

            myresult = c.fetchall()
            print(myresult)
            db.commit()

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
        # Clean up the connection
        connection.close()