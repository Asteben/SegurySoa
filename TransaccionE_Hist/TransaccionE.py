import socket
import sys
import mysql.connector
import json


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('127.0.0.1', 5000)
print('starting up on {} port {}'.format(*server_address))
sock.connect(server_address)


def generate_tx_length(tx_length):
    char_ammount = 5 # Cantidad de caracteres máximos para definir el largo de la transacción (5 según formato solicitado por el bus)
    char_left = char_ammount - len(str(tx_length)) # Espacios sobrantes para rellenar con 0 a la izquierda

    str_tx_length = ''
    for i in range(char_left):
      str_tx_length += '0'
    
    str_tx_length += str(tx_length) # String con el largo de la transacción
    
    return str_tx_length

service_name = 'htrse'

tx_cmd = 'sinit'+ service_name # Comando de registro de servicio ante el bus
tx = generate_tx_length(len(tx_cmd)) + tx_cmd

#sock.send(tx.encode(encoding='UTF-8'))

sock.send('00010sinithtrse'.encode())

status = sock.recv(4096).decode('UTF-8')[10:12] # 'OK' (exitoso) o 'NK' (fallido)

print(status)

# Conexion base de datos
db = mysql.connector.connect(user="root",password="root123",host="localhost",database="mydb1")
c = db.cursor()

a = 0 
while a == 0:
    # Wait for a connection
    print('waiting for a connection')
    #connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        while True:
            aux = sock.recv(250)
            print('received {!r}'.format(aux))

            datos = eval(aux)
            print(datos)
            sql1 = "SELECT Monto, Fecha, Numero_cuenta_destino, Comentario FROM TransaccionEnviada WHERE Cuenta_idCuenta = (%s)"
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

            sock.sendall(brows)
            break
        a = 1
        c.close()
        sock.close()
    finally:
        # Clean up the connection
        sock.close()
db.close()

