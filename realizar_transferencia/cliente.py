import socket
import sys
import json


# Conexión
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 5000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)




try:
    pydata= {#El usuario ingresa los datos
        "Monto": "6000",
        "Comentario": "Rifa perrito, Juan",
        "Cuenta_idCuenta":"013234585",
        "Numero_cuenta_destino":"013232101"
    }
    print("Datos ingresados",pydata)
    #Envía los valores al vus
    jsondata = json.dumps(pydata)
    message = bytes(jsondata, 'utf-8') 
    sock.sendall(message)

    data = b''
    while True:
        data = sock.recv(250)
        print('received {!r}'.format(data))
        break


    if data == b'False_cuenta':
        print ("El número de cuenta no es correcto")
    elif data == b'False_monto':
        print("No se tiene dinero suficiente en su cuenta")
    else:
        Login_user = True
        print (data)

finally:
    print('closing socket')
    sock.close()
