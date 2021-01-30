# import library yg dibutuhkan
import socket
import select
import sys
import os

# mengatur socket server
server_address = ('localhost', 8081)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]
# inisialisasi path
response_path = '.'

# fungsi untuk mendapaatkan body response
# berupa link" dari listdir
def getbody(dirpath):
    files = os.listdir(dirpath)
    body = ""
    for name in files:
        body += '<a href="/' + str(name) + '"> ' + str(name) + ' </a><br>'
    return body

try:
    while True:
        read_ready, write_ready , exception = select.select(input_socket, [], [], 1)
        for sock in read_ready:
            if sock == server_socket:
                # append socket jika client
                client_socket , client_address = server_socket.accept()
                input_socket.append(client_socket)
            else:
                # receive data
                data = sock.recv(4096).decode()
                request_header = data.split('\r\n')

                # jika request header error maka continue
                try:
                    request = request_header[0].split()[1]
                except IndexError:
                    continue
                
                # mereplace string %20 dari request browser menjadi spasi
                # berguna untuk file / folder dengan nama spasi
                request = request.replace("%20"," ")

                # inisialisasi data response
                response_data = ''
                # jika request root maka
                if request == '/':
                    try:
                        # mencari file index.html atau index.php
                        try:
                            f = open('index.html', 'r')
                        except:
                            f = open('index.php', 'r')
                        # jika ketemu read index
                        response_data = f.read()
                        f.close()
                    # jika tidak ada file index maka akan getbody listdir sekarang
                    except:
                        print("index.html Not Found")
                        response_path = "."
                        response_data = getbody(response_path)
                    
                else:
                    # jika meminta parent directory
                    if request == "/updirserver":
                        # pop directory terakhir
                        response_path = response_path.split("/")
                        response_path.pop()
                        response_path = "/".join(response_path)
                        
                        # jika root folder (file server.py ditemukan) maka tidak ada link parentdirectory lagi
                        files = os.listdir(response_path)
                        if "server.py" in files:
                            response_data = getbody(response_path)
                        else:
                            response_data = '<a href="/updirserver"> .. </a><br>' + getbody(response_path)
                    # jika request adalah directory maka akan menambahkan directory req ke path response
                    elif os.path.isdir(response_path + request):
                        response_path += request 
                        # membuat link listdir
                        response_data = '<a href="/updirserver"> .. </a><br>' + getbody(response_path)
                    # jika request berupa file maka akan menampilkan raw file dan mendownloadnya ke directory 
                    # downloadserver pada server.py
                    elif os.path.isfile(response_path + request) :
                        f = open(response_path + request, 'r')
                        f1 = open("./downloadserver"+request, 'w')
                        response_data = f.read()
                        f1.write(response_data)
                        f.close()
                        f1.close()
                        response_data = "<h5>This file has downloaded in downloadserver folder</h5><br>" + response_data
                # mengirimkan response dan header
                content_lenght = len(response_data)
                response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' + str(content_lenght) + "\r\n\r\n"
                sock.sendall(response_header.encode() + response_data.encode())
# keyboard interupt close socket 
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)