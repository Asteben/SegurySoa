import socket
import sys
import json

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 5000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:

    # Send data
    pydata= {
        "Nombre":"pansito5",
        "Email":"pansito5@gmail.com",
        "Password":"pansito123",
        "RUT":"3234585-9",
        "Edad": 552,
        "Telefono": 519645699
    }
    print(pydata)
    jsondata = json.dumps(pydata)
    message = b'' + jsondata
    print('sending {!r}'.format(message))
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()