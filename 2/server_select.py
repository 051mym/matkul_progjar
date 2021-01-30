import socket
import select
import sys
# from datetime import datetime
# import shutil
# import errno

# def copyfile(src, dest):
#     try:
#         shutil.copytree(src, dest)
#     except OSError as e:
#         # If the error was caused because the source wasn't a directory
#         if e.errno == errno.ENOTDIR:
#             shutil.copy(src, dest)
#         else:
#             print('Directory not copied. Error: %s' % e)

server_address = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket,[],[])
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
            else:
                data = sock.recv(1024).decode()
                # print(str(sock.getpeername()), str(data))
                # date = datetime.now()
                if str(data):
                    # client_socket.send(data.encode())
                    f=open( str(data) , "rb")
                    f.seek(0)
                    y=open( "result.txt" , "a+")
                    for line in f:
                        # print(line)
                        # line = str(line)
                        y.write(str(line) + " =" + str(eval(line)))
                        y.write("\n")
                    
                    # f.write( "\n Client Addr = "+ str(client_address) + " Data = " + str(data) + "Date = " + str(date) )
                    
                    # src = data
                    # des = "./serverfile"
                    # copyfile(src,des)
                    # data = sock.recv(1024).decode()
                    # while data :
                    #     data = sock.recv(1024).decode()
                    #     result = eval(data)
                    #     f.write(str(data) + " =" + str(result))

                        



                    





                else:
                    sock.close()
                    input_socket.remove(sock)
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
    f.close()