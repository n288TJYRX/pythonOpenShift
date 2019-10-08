import importlib
import socket
import struct
import re
import pandas
import sys
from ast import literal_eval

from DataInputStream import DataInputStream

# Dynamically import the script
scriptName = importlib.import_module('script2')

HOST = socket.gethostbyname(socket.gethostname())
PORT = 3306
print('Listening for connections from host: ', socket.gethostbyname(
    socket.gethostname()))

scriptInputType = 'JSON'
scriptParameters = None
dictParameters = dict()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    # Setup the port and get it ready for listening for connections
    s.bind((HOST, PORT))
    s.listen(1)
    print('Waiting for incoming connections...')
    conn, addr = s.accept()  # Wait for incoming connections
    conn.sendall(struct.pack('?', True))
    print('Connected to: ', addr)
    dataReceived = False
    while not dataReceived:
        dis = DataInputStream(conn)
        if dis:
            dataReceived = True
            rawData = None
            currentPayload = dis.read_utf()
            while currentPayload != bytes(']', encoding='utf-8'):
                if rawData is None:
                    rawData = bytes() + currentPayload
                else:
                    currentPayload = dis.read_utf()
                    rawData += currentPayload

            # Convert data into the right form based on scriptInputType
            if scriptInputType == 'DATAFRAME':
                data = pandas.read_json(rawData, orient="records", dtype="Object")
            elif scriptInputType == 'JSON':
                data = rawData.decode('utf-8')

            # Run the script passing in the parameters
            data = scriptName.run(data, dictParameters)

            # Convert the data back into JSON
            if isinstance(data, type(pandas.DataFrame([0]))):
                data = pandas.DataFrame.to_json(data, orient="records")

            # Send the results back to the server
            i = 0
            conn.sendall(struct.pack('>i', len(data)))
            if len(data) > 65000:
                splitData = re.findall(('.' * 65000), data)
                while i < (len(data) / 65000) - 1:
                    conn.sendall(struct.pack('>H', 65000))
                    conn.sendall(splitData[i].encode('utf-8'))
                    i += 1
            conn.sendall(struct.pack('>H', len(data) % 65000))
            conn.sendall(data[65000 * i:].encode('utf-8'))
