import socket
import struct
from DataInputStream import DataInputStream

HOST = socket.gethostbyname(socket.gethostname())
PORT = 3306
print('Host is: ', HOST)

def getPort(scriptName):
    return {
        'script1': "30631",
        'script2': "37462",
    }[scriptName]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Setup the port
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    # Wait for incoming connections
    print('Waiting for incoming connections...')
    conn, addr = s.accept()
    print('Connected to: ', addr)
    # Get the script name
    print('Listening for script name...')
    dis = DataInputStream(conn)
    scriptName = dis.read_utf().decode('utf-8')
    print('Script name is: ', scriptName)
    # Send back the right port number based on the script name
    port = getPort(scriptName)
    print('Sending port number: ', port)
    conn.sendall(struct.pack('>H', len(port)))
    conn.sendall(port.encode('utf-8'))
    print('Sent port number.')
