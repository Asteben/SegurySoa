import socket
import sys
import sqlite3

#####CONEXION#######
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('200.14.84.235', 5000)
print('starting up on {} port {}'.format(*server_address))
sock.connect(server_address)
####################

##### Conexion base de datos #####
conn = sqlite3.connect('banco.sqlite')
cur = conn.cursor()
####################

a = 0 #Esto es basicamente hacer el stop al while.

###################
def generate_tx_length(tx_length):
    char_ammount = 5 # Cantidad de caracteres máximos para definir el largo de la transacción (5 según formato solicitado por el bus)
    char_left = char_ammount - len(str(tx_length)) # Espacios sobrantes para rellenar con 0 a la izquierda

    str_tx_length = ''
    for i in range(char_left):
      str_tx_length += '0'
    
    str_tx_length += str(tx_length) # String con el largo de la transacción
    
    return str_tx_length

service_name = 'pserv'

tx_cmd = 'sinit'+ service_name # Comando de registro de servicio ante el bus
tx = generate_tx_length(len(tx_cmd)) + tx_cmd

sock.send(tx.encode(encoding='UTF-8'))

status = sock.recv(4096).decode('UTF-8')[10:12] # 'OK' (exitoso) o 'NK' (fallido)

print(status)

###################

while True:

    print('waiting for a connection')
    #connection, client_address = sock.accept()
    try:
        while True:
            aux1 = sock.recv(250)
            aux = aux1[10:]
            datos = eval(aux) #Datos recibidos"
            print("DATOS RECIBIDOS DEL CLIENTE:",datos)

            data_search = (datos['Rut'],datos['Id_login'],datos['Servicio'],datos['Tipo_cuenta'],datos['Monto'],)
            cur.execute('SELECT Saldo, idCuenta FROM Cuenta  WHERE Cuenta.tipo_idTipo = ? AND Cuenta.Usuario_idUsuario = ?',(datos['Tipo_cuenta'],datos['Id_login'],))
            myresult = cur.fetchall()
            saldo_cuenta = myresult[0][0]
            id_cuenta = myresult[0][1]
            conn.commit()

            if datos['Monto'] <= saldo_cuenta:
            	print("Se puede pagar:")
            	cur.execute('SELECT Saldo, idServicio  FROM Servicio WHERE Servicio.Nombre = ?',(datos['Servicio'],))
            	myresult = cur.fetchall()
            	saldo = myresult[0][0]
            	id_servicio = myresult[0][1]
            	conn.commit()
            	cur.execute('UPDATE Servicio SET Saldo = ? WHERE Nombre = ?' ,(datos['Monto']+saldo, datos['Servicio'],))
            	conn.commit()
            	cur.execute('UPDATE Cuenta SET Saldo = ? WHERE tipo_idTipo = ? AND Usuario_idUsuario = ?',(saldo_cuenta-datos['Monto'],datos['Tipo_cuenta'],datos['Id_login'],))
            	conn.commit()
            	cur.execute('INSERT INTO Pago (Monto, Fecha,Cuenta_idcuenta, Servicio_idservicio) VALUES (?, ?, ?, ?)',(datos['Monto'],"asd",id_cuenta,id_servicio,))
            	conn.commit()
            	tx_cmd = service_name + 'True' # Comando de registro de servicio ante el bus
            	tx = generate_tx_length(len(tx_cmd)) + tx_cmd
            	sock.send(tx.encode(encoding='UTF-8'))
            else:
            	print("No hay saldo suficiente")
            	tx_cmd = service_name + 'False' + 'Saldo no suficiente para pagar' # Comando de registro de servicio ante el bus
            	tx = generate_tx_length(len(tx_cmd)) + tx_cmd
            	sock.send(tx.encode(encoding='UTF-8'))
            break

    finally:
    	print("finally")
sock.close()

