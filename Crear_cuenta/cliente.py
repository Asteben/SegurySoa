import socket
import sys
import json


####CONEXIÓN
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 5000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)




try:
    pydata = { ##datos ingresados por el usuario
        "Numero":"19648854",
        "Usuario_idUsuario":"mannymanito",
        "Tipo_idTipo":"1"
    }
    print("Valores ingresados:", pydata)
    ##Envía paquetes al servicio
    jsondata = json.dumps(pydata)
    message = bytes(jsondata, 'utf-8') 
    sock.sendall(message)

    data = b''
    while True:#espera una respuesta
        data = sock.recv(250)
        print('received {!r}'.format(data))
        break


    if data == b'False':
        print("Ya existe una cuenta con este número")

    else:
        #redirigir a informaciónCuenta
        print("Cuenta creada con éxito")
        print(data)


finally:
    print('closing socket')
    sock.close()
