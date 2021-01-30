import socket

server_address = ('localhost', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "hello ucup"
client_socket.sendto(message.encode(), server_address)

recv_message, server_address = client_socket.recvfrom(1024)
print('message > ' + str(recv_message.decode()) + ' server_address > ' + str(server_address))