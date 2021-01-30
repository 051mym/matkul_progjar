import socket
import select
import sys
# import os

server_address = ('127.0.0.1', 8000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]
try:
    while True:
        read_ready, wread_ready , exception = select.select(input_socket,[],[])
        for sock in read_ready:
            if sock == server_socket:
                client_socket , address_client = server_socket.accept()
                input_socket.append(client_socket)
            else:
                # menerima data sampai null
                data = sock.recv(4096).decode()
                print(data)

                request_header = data.split('\r\n')
                request_file = request_header[0].split()[1]

                if request_file == 'index.html' or request_file == '/':
                    # print( os.listdir() )
                    f = open('index.html', 'r')
                    response_data = f.read()
                    f.close()

                    content_lenght = len(response_data)
                    response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; \
                         charset=UTF-8\r\nContent-Lenght:' + str(content_lenght)
                    sock.sendall(response_header.encode() + response_data.encode())
                
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)