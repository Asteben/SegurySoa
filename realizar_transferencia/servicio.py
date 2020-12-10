import socket
import sys
import sqlite3
import datetime


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
            print('received {!r}'.format(aux))

            datos = eval(aux)
            print(datos)
            sql = "SELECT Saldo FROM Cuenta WHERE cuenta.Cuenta_idCuenta = %s ;"
            data_search = (datos['Cuenta_idCuenta'],)
            cur.execute(sql, data_search)

            myresult = cur.fetchall()
            print(myresult)
            conn.commit()


            if len(myresult): #si existe la cuenta
                if myresult[0][0] > int(datos['Monto']):

                    sql = "SELECT Saldo, idCuenta FROM Cuenta WHERE idCuenta = %s ;"  #modifica saldo cuenta destino
                    cur.execute(sql,datos['Cuenta_idCuenta'],)
                    myresult = cur.fetchall()
                    saldo = myresult[0][0]
                    cuenta = myresult[0][1]
                    conn.commit()

                    sql = "UPDATE  Cuenta SET saldo = %s WHERE idCuenta = %s ;"
                    cur.execute(sql,int(datos['Monto'])+saldo,datos['Numero_cuenta_destino'],)
                    conn.commit()

                    sql = "SELECT Saldo, idCuenta FROM cuenta WHERE cuenta.idcuenta = %s ;"  #modifica saldo cuenta origen
                    cur.execute(sql,datos['idCuenta'],)
                    myresult = cur.fetchall()
                    saldo = myresult[0][0]
                    cuenta = myresult[0][1]
                    conn.commit()

                    sql = "UPDATE Cuenta SET Saldo = %s WHERE idCuenta = %s ;"
                    cur.execute(sql,saldo - int(datos['Monto']),datos['Cuenta_idCuenta'],)
                    conn.commit()


                    sql = "INSERT INTO TransaccionEnviada (Monto, Comentario, Fecha, Cuenta_idCuenta, Numero_cuenta_destino) VALUES (%s, %s,%s, %s, %s)"  #inserta en pagos
                    x = datetime.datetime.now()
                    val = ( datos['monto'], datos['Comentario'], x, datos['Cuenta_idCuenta'], datos['Numero_cuenta_destino'])
                    cur.execute(sql, val)
                    conn.commit()
                else:
                    sock.sendall(b'False_monto')
                break

            else:
                sock.sendall(b'False_cuenta')
            break

        a = 1
        connection.close()

    finally:
        # Clean up the connection
        connection.close()