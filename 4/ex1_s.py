import socket
import select
import sys
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
ip_address = 'localhost'
port = 8081
server.bind((ip_address,port))
server.listen(100)
list_of_client=[]

def clientthread(conn,addr):
    while True:
        try:
            message = conn.recv(2048).decode()
            if message:
                # print('<' + addr[0] + '> ' + message)
                message_to_send = '<' + addr[0] + '> ' + message
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue

def broadcast(message , connection):
    for client in list_of_client:
        if client != connection:
            try:
                client.send(message.encode())
            except:
                client.close()
                remove(client)

def remove(connection):
    if connection in list_of_client:
        list_of_client.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_client.append(conn)
    print('Adress: ' + addr[0] + ' connected')
    threading.Thread(target=clientthread,args=(conn,addr)).start()

conn.close()
