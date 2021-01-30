import socket
import time
import sys
import threading 

def print_msg():
    while True:
        recv_msg = client_socket.recv(1024).decode()
        msg_usr = recv_msg.split()[:2]
        user = str(client_socket.getsockname())
        user = user.split()
        if msg_usr == user:
            continue
        else:
            print(str(recv_msg).rjust(79))
            # print( str(recv_msg) )

server_address = ('localhost', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(server_address)

if __name__ == "__main__":
    t1 = threading.Thread(target=print_msg)
    t1.start()

    while True:
        message = sys.stdin.readline() 
        message = str(client_socket.getsockname()) + ' ' + message 
        client_socket.send(message.encode())
