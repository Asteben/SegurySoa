import socket
import sys
#import MySQLdb

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('127.0.0.1', 5000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Conexión base de datos
#db=MySQLdb.connect(host="localhost",user="root",passwd="root123",db="mydb")
#c = db.cursor(MySQLdb.cursors.DictCursor)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        data = b''
        while True:
            aux = connection.recv(16)
            data= data + aux
            print('received {!r}'.format(aux))
            connection.sendall(aux)
            if aux == b'' :
                print('no data from', client_address)
                print(data)
                #connection.sendall(data)
                break

    finally:
        # Clean up the connection
        connection.close()