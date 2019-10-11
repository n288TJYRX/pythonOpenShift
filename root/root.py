import socket
from DataInputStream import DataInputStream

HOST = socket.gethostbyname(socket.gethostname())
PORT = 3306
print('Host is: ', HOST)

def getPort(scriptName):
    return {
        'script1': "37572",
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
    dis = DataInputStream(conn)
    scriptName = dis.read_utf().decode('utf-8')
    # Send back the right port number based on the script name
    port = getPort(scriptName)
    conn.sendall(port.encode('UTF-8')) 
