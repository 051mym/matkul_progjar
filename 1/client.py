import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5005))
client.send("I am CLIENT\n".encode())
from_server = client.recv(4096).decode()
client.close()
print(from_server)