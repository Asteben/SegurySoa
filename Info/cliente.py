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
        "Rut":"3234585-9",
    }
    print(pydata)
    jsondata = json.dumps(pydata)
    message = bytes(jsondata, 'utf-8') 
    print('sending {!r}'.format(message))
    sock.sendall(message)

    data = b''
    while True:
        data = sock.recv(250)
        print('received {!r}'.format(data))
        #print(data)
        break


    if data == b'False':
        print ("no se pudo logar")

    else:
        Login_user = True
        print ( data)

finally:
    print('closing socket')
    sock.close()