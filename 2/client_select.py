import socket
import sys


server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# sys.stdout.write(' >> ')

try:
    while True:
        message = str(input())
        client_socket.send("soal.txt".encode())
        # f=open( "soal.txt" , "rb")
        # f.seek(0)
        # for line in f:
        #     # print(line)
        #     line = str(line)
        #     client_socket.send(line.encode())
        # print("hey")
        # client_socket.send("NULL".encode())


        # sys.stdout.write(client_socket.recv(1024).decode())
        # sys.stdout.write(' >> ')

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)