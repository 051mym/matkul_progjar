import socket

server_address = ('localhost', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(server_address)

message = 'haii...'
delay = 1

while True:
    client_socket.send(message.encode())
    client_socket.settimeout(delay)

    try:
        recv_msg = client_socket.recv(1024).decode()
        print( str(recv_msg) + ' delay : ' + str(delay))
    except socket.timeout:
        # print('server_down')
        delay *= 2
        if delay > 2:
            print('server down')
        else:
            break