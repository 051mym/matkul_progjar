import socket
import sys
from datetime import datetime

server_address = ('localhost', 6001)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

try:
    while True :
        client_socket, client_address = server_socket.accept()
        # print("client socket = ", client_socket)
        # print("client address = ", client_address)

        dataf = client_socket.recv(1024).decode()
        # date = datetime.now()

        # string = "Ok send " + str(client_address)+ " " + data + " " + str(date)
        # + str(client_socket)
        # + str(client_socket) + str(client_address)
        # client_socket.send(string.encode())
        print(dataf)
        f=open( "..\\" +str(dataf) , "a+")
        # string = f.read()

        # print(str(data))
        string = client_socket.recv(1024).decode()
        print(string)
        # log = 'log.txt'
        # f= open("log.txt","a+")
        f.write("server " + string)
        # f.write( "\n Client Addr = "+ str(client_address) + " Data =" + str(data))
        f.close() 
        # f.write(str(client_address))
        # f.write(data)
        # , client_address, data
        # f.read()
        client_socket.close()

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)




