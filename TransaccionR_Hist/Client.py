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
        "idCuenta": 2
    }

    jsondata = json.dumps(pydata)
    bjson = b'' + jsondata
    sock.sendall(bjson)

    data = b''
    while True:
        data = sock.recv(250)
        dataeval = eval(data)
        print("Las transacciones recividas historicamente son:")
        aux = 0
        while aux < len(dataeval):
            print(aux,"- Numero de cuenta origen:",dataeval[aux][2],"Monto:",dataeval[aux][0],"Fecha:",dataeval[aux][1],"Comentario:",dataeval[aux][3])
            aux = aux + 1
        break

finally:
    print('closing socket')
    sock.close()