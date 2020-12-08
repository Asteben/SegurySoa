import socket
import sys
import json

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 5000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

Login_user = False

try:

    pydata= {
        "idCuenta": 1
    }

    jsondata = json.dumps(pydata)
    bjson = b'' + jsondata
    sock.sendall(bjson)

    data = b''
    while True:
        data = sock.recv(250)
        dataeval = eval(data)
        print("Los Pagos efectuados historicamente son:")
        aux = 0
        while aux < len(dataeval):
            print(aux,"- Servicio:",dataeval[aux][0],"Monto:",dataeval[aux][1],"Fecha:",dataeval[aux][2])
            aux = aux + 1
        break

finally:
    print('closing socket')
    sock.close()