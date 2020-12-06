import socket
import sys
import json


#####CONEXION#######
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 5000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
####################

Login_user = False   #FALSE -> Usuario desconectado, TRUE -> Usuario conectado

try:
    pydata= {  #Datos para iniciar sesion
        "Email":"pansito5@gmail.com",
        "Password":"pansito123",
    }

    jsondata = json.dumps(pydata)  
    message = bytes(jsondata, 'utf-8') 
    sock.sendall(message)   #Envia paquete al servicio


    while True: #Espera hasta recibir la respuesta por parte del serivico
        data = sock.recv(250)
        print('received {!r}'.format(data))
        print(data)
        break


    if data == b'False': #Respuesta False -> No se pudo logear
        print ("no se pudo logar")

    else:
        Login_user = True #De lo contrario, se logea.
        print ( "Logeado")

finally:
    print('closing socket') #end
    sock.close()