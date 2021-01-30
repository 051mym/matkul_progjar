import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8000)
client_socket.connect(server_address)

request_header = 'GET / HTTP/1.0\r\n Host : localhost\r\n\r\n'
client_socket.send(request_header.encode())

response = ''
while True:
    recv = client_socket.recv(1024).decode()
    if recv == "end":
        print("hello")
        break
    response += recv
    # print(recv)

print(response)
client_socket.close()