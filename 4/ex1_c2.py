import socket
import select
import sys
# import msvcrt

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = 'localhost'
port = 8081
server.connect((ip_address,port))

while True:
    sockets_list = [sys.stdin,server]
    read_socket, write_socket, error_socket = select.select(sockets_list,[],[])
    
    for sock in read_socket:
        if sock == server:
            message = sock.recv(2048)
            # print(message)
            f = open('recv_client2.txt', 'w')
            f.write(message.decode())
            f.close()

        else:
            message = sys.stdin.readline()

            filenya = message
            f = open(filenya[0:-1])
            file_send = f.read()

            server.send(file_send.encode())
            f.close()

            # server.send(message.encode()) ##
            sys.stdout.write('< Yusuf > ')
            sys.stdout.write(message)
            sys.stdout.flush()

server.close()
