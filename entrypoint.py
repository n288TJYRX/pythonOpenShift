import socket
import struct
import time
from DataInputStream import DataInputStream

HOST = socket.gethostbyname(socket.gethostname())
PORT = 3306
print('Listening for connections from host: ', socket.gethostbyname(
    socket.gethostname()))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Setup the port and get it ready for listening for connections
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print('Waiting for incoming connections...')
    # Wait for incoming connections
    conn, addr = s.accept()  
    conn.sendall('Connected to the python server!'.encode('utf-8'))
    print('Connected to: ', addr)
    # Keep listening for requests to run scripts
        # if dis:
            # # Check the data is in the right format
            # data = dis.read_utf()

            # # Run the right script passing in the parameters
            # # (Do nothing with the data at the moment)

            # # Send the results back to the server
            # # (At the moment just send the data back)
            # if data:
            #     conn.sendall(data.encode('utf-8'))
