import socket
import sys
import sqlite3


#####conexión
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('200.14.84.235', 5000)
print('starting up on {} port {}'.format(*server_address))
sock.connect(server_address)
######


#####Conexion base de datos
conn = sqlite3.connect('banco.sqlite')
cur = conn.cursor()
######

###################
def generate_tx_length(tx_length):
    char_ammount = 5 # Cantidad de caracteres máximos para definir el largo de la transacción (5 según formato solicitado por el bus)
    char_left = char_ammount - len(str(tx_length)) # Espacios sobrantes para rellenar con 0 a la izquierda

    str_tx_length = ''
    for i in range(char_left):
      str_tx_length += '0'
    
    str_tx_length += str(tx_length) # String con el largo de la transacción
    
    return str_tx_length

service_name = 'rtran'

tx_cmd = 'sinit'+ service_name # Comando de registro de servicio ante el bus
tx = generate_tx_length(len(tx_cmd)) + tx_cmd

sock.send(tx.encode(encoding='UTF-8'))

status = sock.recv(4096).decode('UTF-8')[10:12] # 'OK' (exitoso) o 'NK' (fallido)

print(status)

###################


a = 0 
while a == 0:
    #espera una conexión
    print('waiting for a connection')
    #connection, client_address = sock.accept()
    try:
        # Receive the data in small chunks and retransmit it
        while True:
            aux1 = sock.recv(250)
            aux = aux1[10:]

            datos = eval(aux)
            print(datos)

            sql = "SELECT Saldo FROM Cuenta WHERE idCuenta = ? ;"
            data_search = (datos['cuenta'],)
            cur.execute(sql, data_search)

            myresult = cur.fetchall()
            print(myresult)
            conn.commit()


            if len(myresult): #si existe la cuenta
                if myresult[0][0] > int(datos['monto']):

                    sql = "SELECT Saldo, idCuenta FROM Cuenta WHERE Numero = ? ;"  #modifica saldo cuenta destino
                    cur.execute(sql,datos['cuentadestino'],)
                    myresult = cur.fetchall()
                    saldo = myresult[0][0]
                    cuentad = myresult[0][1]
                    conn.commit()

                    sql = "UPDATE  Cuenta SET saldo = ? WHERE idCuenta = ? ;"
                    cur.execute(sql,int(datos['monto'])+saldo, cuentad,)
                    conn.commit()

                    sql = "SELECT Saldo, Numero FROM Cuenta WHERE idCuenta = ? ;"  #modifica saldo cuenta origen
                    cur.execute(sql,datos['cuenta'],)
                    myresult = cur.fetchall()
                    saldo = myresult[0][0]
                    numero = myresult[0][1]
                    conn.commit()

                    sql = "UPDATE Cuenta SET Saldo = ? WHERE idCuenta = ? ;"
                    cur.execute(sql,saldo - int(datos['monto']),datos['cuenta'],)
                    conn.commit()


                    sql = "INSERT INTO TransaccionEnviada (Monto, Comentario, Fecha, Cuenta_idCuenta, Numero_cuenta_destino) VALUES (%s, %s,%s, %s, %s)"  #inserta en envio
                    val = ( datos['monto'], datos['comentario'], datos['fecha'], datos['cuenta'], datos['cuentadestino'],)
                    cur.execute(sql, val)
                    conn.commit()

                    sql = "INSERT INTO TransaccionRecibida (Monto, Comentario, Fecha, Cuenta_idCuenta, Numero_cuenta_origen) VALUES (%s, %s,%s, %s, %s)"  #inserta en recibido
                    val = ( datos['monto'], datos['comentario'], datos['fecha'], cuentad, numero,)
                    cur.execute(sql, val)
                    conn.commit()


                    ##Envia un true
                    tx_cmd = service_name + 'True'
                    tx = generate_tx_length(len(tx_cmd)) + tx_cmd
                    sock.send(tx.encode(encoding='UTF-8'))
                else:
                    ##Envia un falsesaldo
                    tx_cmd = service_name + 'Falsesaldo'
                    tx = generate_tx_length(len(tx_cmd)) + tx_cmd
                    sock.send(tx.encode(encoding='UTF-8'))
                break

            else:
                ##Envia un faslecuenta
                tx_cmd = service_name + 'Falsecuenta'
                tx = generate_tx_length(len(tx_cmd)) + tx_cmd
                sock.send(tx.encode(encoding='UTF-8'))
            break

        a = 1
        sock.close()

    finally:
        # Clean up the connection
        sock.close()