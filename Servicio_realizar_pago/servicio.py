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

service_name = 'rpago'

tx_cmd = 'sinit'+ service_name # Comando de registro de servicio ante el bus
tx = generate_tx_length(len(tx_cmd)) + tx_cmd

sock.send(tx.encode(encoding='UTF-8'))

status = sock.recv(4096).decode('UTF-8')[10:12] # 'OK' (exitoso) o 'NK' (fallido)

print(status)

###################


a = 0 
while a == 0:
    # Wait for a connection
    print('waiting for a connection')
    ##connection, client_address = sock.accept()
    try:
        while True:
            aux1 = sock.recv(250)
            aux = aux1[10:]
            datos = eval(aux)
            print(datos)

            #Se verifica si hay saldo en la cuenta emisora
            sql = "SELECT saldo FROM cuenta WHERE cuenta.idcuenta = %s ;"
            data_search = (datos['cuenta'],)
            cur.execute(sql, data_search)

            myresult = cur.fetchall()
            print(myresult)
            conn.commit()


            if len(myresult):#Si existe el resultado
                if myresult[0][0] > int(datos['monto']):#Si hay dinero suficiente

                    sql = "SELECT saldo, idServicio FROM servicio WHERE nombre = %s ;"  #modifica saldo servicio
                    cur.execute(sql,datos['servicio'],)
                    myresult = cur.fetchall()
                    saldo = myresult[0][0]
                    servicio = myresult[0][1]
                    conn.commit()

                    sql = "UPDATE servicio SET saldo = %s WHERE servicio = %s ;"
                    cur.execute(sql,int(datos['monto'])+saldo,datos['servicio'],)
                    conn.commit()

                    sql = "SELECT saldo, idCuenta FROM cuenta WHERE cuenta.idcuenta = %s ;"  #modifica saldo cuenta
                    cur.execute(sql,datos['cuenta'],)
                    myresult = cur.fetchall()
                    saldo = myresult[0][0]
                    cuenta = myresult[0][1]
                    conn.commit()

                    sql = "UPDATE cuenta SET saldo = %s WHERE cuenta.idcuenta = %s ;"
                    cur.execute(sql,saldo - int(datos['monto']),datos['cuenta'],)
                    conn.commit()


                    sql = "INSERT INTO pago (monto, fecha, cuenta_idcuenta, servicio_idservicio) VALUES (%s, %s,%s, %s)"  #inserta en pagos
                    val = ( datos['monto'], datos['fecha'] , datos['cuenta'] , datos['servicio'] )
                    cur.execute(sql, val)
                    conn.commit()

                    ##Envia un true
                    tx_cmd = service_name + 'True'
                    tx = generate_tx_length(len(tx_cmd)) + tx_cmd
                    sock.send(tx.encode(encoding='UTF-8'))

            else:
                tx_cmd = service_name + 'False' #Envia un false
                tx = generate_tx_length(len(tx_cmd)) + tx_cmd
                sock.send(tx.encode(encoding='UTF-8'))
            break

        a = 1
        sock.close()

    finally:
        # Clean up the connection
        sock.close()