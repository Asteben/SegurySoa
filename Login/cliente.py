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
        "Email":"sujeto1@gmail.com",
        "Password":"sujeto123",
    }
    jsondata = json.dumps(pydata)
    bjson = b'' + jsondata
    #message = bytes(jsondata, 'utf-8') 
    #print('sending {!r}'.format(jsdondata))
    sock.sendall(bjson)

    data = b''
    while True:
        data = sock.recv(250)
        print('received {!r}'.format(data))
        print(data)
        break


    if data == b'False':
        print ("no se pudo logar")

    else:
        Login_user = True
        print ( "Logeado")

finally:
    print('closing socket')
    sock.close()