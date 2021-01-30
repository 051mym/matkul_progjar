# import library yg dibutuhkan
import socket
import time
import sys
import threading
import select
import os
import zipfile

# fungsi receive file
def recv_file(fname):
    f = open(fname, 'wb')
    while True:
        ready = select.select([client_socket], [], [], 3)
        if ready[0]:
            data, addr = client_socket.recvfrom(1024)
            f.write(data)
        else:
            f.close()
            break

#fungsi send file
def send_file(fname):
    f = open(fname, "rb")
    data = f.read(1024)
    while(data):
        if( client_socket.send( data ) ):
            data = f.read(1024)
            time.sleep(0.02) # Give receiver a bit time to save
    f.close()

# fungsi untuk mencetak message yg dikirim server
# fungsi ini akan dijalankan oleh thread
def print_msg():
    while True:
        recv_msg = client_socket.recv(1024).decode()
        print(str(recv_msg).rjust(80))
        if recv_msg.split()[2] == "SEND":
            recv_file(recv_msg.split()[3])
        elif recv_msg.split()[2] == "UPTRACT":
            recv_file(recv_msg.split()[3].replace('/','-')+'.zip')

# buat socket client dan menghubungkan ke server
server_address = ('localhost', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(server_address)

if __name__ == "__main__":
    # thread untuk print message
    t1 = threading.Thread(target=print_msg)
    
    # mengirimkan connect jika awal konek server
    message = str(client_socket.getsockname()) + ' ' + 'connect'
    client_socket.send(message.encode())
    recv_msg = client_socket.recv(1024).decode()
    print(recv_msg)
    
    t1.start()



    while True:
        try:
            # read inputan pada terminal
            message = sys.stdin.readline() 
            message = str(client_socket.getsockname()) + ' ' + message 
            client_socket.send(message.encode())

            # jika kata kunci SEND maka akan melakukan fungsi send file ke server
            if message.split()[2] == "SEND":
                send_file(message.split()[3])
            # jika kata kunci UPTRACT maka akan melakukan fungsi send file zip dari folder
            elif message.split()[2] == "UPTRACT":
                # melakukan zip folder
                path = message.split()[3]
                zipname = message.split()[3].replace('/','-') + '.zip' 
                # print(zipname)
                zf = zipfile.ZipFile(zipname, "w")
                for dirname, subdirs, files in os.walk(path):
                    zf.write(dirname)
                    for filename in files:
                        zf.write(os.path.join(dirname, filename))
                zf.close()

                #send file
                send_file(zipname)
                os.remove(zipname)

        except KeyboardInterrupt:
            print('you left the chat')
            message = str(client_socket.getsockname()) + ' ' + 'closed'
            client_socket.send(message.encode())
            client_socket.close()
            sys.exit(0)
            break
        

        
            

