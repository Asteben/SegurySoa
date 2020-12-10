import socket
import sys
import sqlite3
import json

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

service_name = 'login'

tx_cmd = 'sinit'+ service_name # Comando de registro de servicio ante el bus
tx = generate_tx_length(len(tx_cmd)) + tx_cmd

sock.send(tx.encode(encoding='UTF-8'))

status = sock.recv(4096).decode('UTF-8')[10:12] # 'OK' (exitoso) o 'NK' (fallido)

print(status)

###################

while a == 0:

    print('waiting for a connection')
    #connection, client_address = sock.accept()
    try:
        while True:
            aux1 = sock.recv(250)
            aux = aux1[10:]
            datos = eval(aux) #Datos recibidos"
            print("DATOS RECIBIDOS DEL CLIENTE:",datos)


            #********* Consulta BDD **********
            data_search = (datos['Email'],datos['Password'])
            cur.execute('SELECT idUsuario, RUT FROM Usuario  WHERE Usuario.Email = ? AND Usuario.Password = ? ',data_search)
            myresult = cur.fetchall()
            print("DATOS ENCONTRADOS:",myresult)
            conn.commit()
            #********************


            if len(myresult): #si hay algo en el select, entonces existe la cuenta
                print("Logeado")
                #connection.sendall(b'True')
                
                jrows = json.dumps(myresult,default=str)
                tx_cmd = service_name + 'True' + jrows # Comando de registro de servicio ante el bus
                tx = generate_tx_length(len(tx_cmd)) + tx_cmd
                sock.send(tx.encode(encoding='UTF-8'))
            else:
                print("Error")
                tx_cmd = service_name + 'False' # Comando de registro de servicio ante el bus
                tx = generate_tx_length(len(tx_cmd)) + tx_cmd
                sock.send(tx.encode(encoding='UTF-8'))
            break

        a = 1
        sock.close()

    finally:
        sock.close()