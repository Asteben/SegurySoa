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
            sql = "SELECT saldo FROM cuenta WHERE cuenta.idcuenta = %s ;"
            data_search = (datos['idCuenta'],)
            c.execute(sql, data_search)

            myresult = c.fetchall()
            print(myresult)
            db.commit()


            if len(myresult):
                if myresult[0][0] > int(datos['monto']):

                    sql = "SELECT saldo, idServicio FROM servicio WHERE nombre = %s ;"  #modifica saldo servicio
                    c.execute(sql,data['servicio'],)
                    myresult = c.fetchall()
                    saldo = myresult[0][0]
                    servicio = myresult[0][1]
                    db.commit()

                    sql = "UPDATE servicio SET saldo = %s WHERE servicio = %s ;"
                    c.execute(sql,int(data['monto'])+saldo,data['servicio'],)
                    db.commit()

                    sql = "SELECT saldo, idCuenta FROM cuenta WHERE cuenta.idcuenta = %s ;"  #modifica saldo cuenta
                    c.execute(sql,datos['idCuenta'],)
                    myresult = c.fetchall()
                    saldo = myresult[0][0]
                    cuenta = myresult[0][1]
                    db.commit()

                    sql = "UPDATE cuenta SET saldo = %s WHERE cuenta.idcuenta = %s ;"
                    c.execute(sql,saldo - int(data['monto']),data['idCuenta'],)
                    db.commit()


                    sql = "INSERT INTO pago (monto, fecha,cuenta_idcuenta, servicio_idservicio) VALUES (%s, %s,%s, %s)"  #inserta en pagos
                    val = ( datos['monto'], 03032020 , cuenta , servicio )
                    mycursor.execute(sql, val)
                    db.commit()

            else:
                sock.sendall(b'False')
            break

        a = 1
        connection.close()

    finally:
        # Clean up the connection
        connection.close()