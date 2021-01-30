import socket
ip    = input("Enter Ip > ")
port    = int(input("Enter port > "))
namefile = input("Enter nama file > ")

server_address = (ip, port)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# string = "Am I Client?"
f=open(namefile , "r")
string = f.read()
print(string)
client_socket.send(namefile.encode())

client_socket.send(string.encode())



# data = client_socket.recv(1024).decode()
# print(data)
# client_socket.close()