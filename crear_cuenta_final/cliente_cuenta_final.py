import socket
import sys
import json


#####CONEXION#######
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 5000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
####################


try:
    pydata= {
        "Nombre":"pansito5",
        "Email":"pansito5@gmail.com",
        "Password":"pansito123",
        "RUT":"3234585-9",
        "Edad": 552,
        "Telefono": 519645699
    }

    jsondata = json.dumps(pydata)  
    message = bytes(jsondata, 'utf-8') 
    sock.sendall(message)   #Envia paquete al servicio

    while True: #Espera hasta recibir la respuesta por parte del serivico
        data = sock.recv(250)
        print('received {!r}'.format(data))
        print(data)
        break


    if data == b'False': #Respuesta False -> No se pudo crear cuenta
        print ("no se pudo crear la cuenta")

    else:
        Login_user = True #De lo contrario, se crea cuenta.
        print ( "Cuenta creada")

finally:
    print('closing socket') #end
    sock.close()