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

service_name = 'crear'

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


            #********* Crear usuario BDD **********
            data_search = (datos['Nombre'],datos['Email'],datos['Password'],datos['RUT'],datos['Edad'],datos['Telefono'])
            cur.execute('INSERT INTO Usuario (Nombre, Email, Password, Rut, Edad, Telefono) VALUES (?, ?, ?, ?, ?, ?)',data_search)
            conn.commit()
            
            cur.execute('SELECT * FROM usuario') #Esto solo sirve para mostrar todos los usuarios de la bdd
            myresult = cur.fetchall()
            print("DATOS ENCONTRADOS:",myresult)
            conn.commit()
            #********************

            #connection.sendall(b'True')
            tx_cmd = service_name + 'True' # Comando de registro de servicio ante el bus
            tx = generate_tx_length(len(tx_cmd)) + tx_cmd
            sock.send(tx.encode(encoding='UTF-8'))
            break



    finally:
        print("finally")
sock.close()
