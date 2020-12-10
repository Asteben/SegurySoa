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
        "Rut":"111111",
    }

    jsondata = json.dumps(pydata)  
    message = bytes(jsondata, 'utf-8') 
    sock.sendall(message)   #Envia paquete al servicio

    data = b''

    while True: #Espera hasta recibir la respuesta por parte del serivico
        data = sock.recv(250)
        break


    if data == b'False': #Respuesta False -> No se pudo crear cuenta
        print ("ERROR, no hay datos")
    else:
        print ( "DATOS:")
        print(data)

finally:
    print('closing socket') #end
    sock.close()