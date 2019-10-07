import socket
import struct
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
    conn.sendall(struct.pack('?', True))
    print('Connected to: ', addr)
    # Keep listening for requests to run scripts
    while True:
        dis = DataInputStream(conn)
        if dis:
            # Check the data is in the right format
            currentPayload = dis.read_utf()
            while currentPayload != bytes(']', encoding='utf-8'):
                if rawData is None:
                    rawData = bytes() + currentPayload
                else:
                    currentPayload = dis.read_utf()
                    rawData += currentPayload
            data = rawData.decode('utf-8')

            # Run the right script passing in the parameters
            # (Do nothing with the data at the moment)

            # Send the results back to the server
            # (At the moment just send the data back)
            conn.sendall(data.encode('utf-8'))
