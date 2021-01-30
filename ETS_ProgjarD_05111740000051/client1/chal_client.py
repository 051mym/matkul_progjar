# import library yg dibutuhkan
import socket
import time
import sys
import threading
import select
import os
import zipfile
from ftplib import FTP
import shutil

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
        
        if recv_msg.split()[2] == "SENDALL":
            recv_file(recv_msg.split()[3])
            continue

        print(str(recv_msg).rjust(80))

# buat socket client dan menghubungkan ke server
server_address = ('localhost', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(server_address)

if __name__ == "__main__":

    print('Input user ftp: ') 
    user = input()
    print('Input password ftp: ')
    pswd = input()
    print('Input IP FTP: ')
    ipftp = input()

    f = FTP(ipftp)
    f.login(user, pswd)

    act1 = 'LIST'
    act2 = 'PWD'
    act3 = 'CD'
    act4 = 'MKDIR'
    act5 = 'SENDALL'
    act6 = 'DOWNZIP'

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
            # client_socket.send(message.encode()) loloolo

            if message.split()[2] == "SENDALL":
                inpt2 = message.split()[3]
                f.retrbinary("RETR " + inpt2, open(inpt2, 'wb').write)

                send_file(inpt2)
                client_socket.send(message.encode())
            else :

                if message.split()[2].count(act1) == 1:
                    names = f.nlst()                                        #LIST DIRECTORY
                    print('List : ' + str(names))

                elif message.split()[2].count(act2) == 1:
                    print('PWD :' + f.pwd())           #PRESENT WORK DIRECTORY

                # elif message.split()[2].count(act2) == 1:                               
                #     inpt2 = message.split()[2].replace('RETR ', '')                        #DOWNLOAD   
                #     f.retrbinary("RETR " + inpt2, open(inpt2, 'wb').write)

                
                # elif message.split()[2].count(act3) == 1:
                #     inpt2 = message.split()[2].replace('STOR ', '')
                #     f.storbinary('STOR ' + inpt2, open(inpt2, 'rb'))              #UPLOAD


                elif message.split()[2].count(act3) == 1:
                    inpt2 = message.split()[3]
                    f.cwd(inpt2)                                                   #CD
                    
                elif message.split()[2].count(act4) == 1:
                    inpt2 = message.split()[3]                                         
                    f.mkd(inpt2)                                               #BUAT DIRECTORY
                
                elif message.split()[2].count(act5) == 1:
                    print('PWD :' + f.pwd())           #PRESENT WORK DIRECTORY

                elif message.split()[2].count(act6) == 1:                               #DOWNPRESS (FILE DIRECTORY DIUBAH SECARA MANUAL)
                    inpt2 = message.split()[3] 
                    shutil.make_archive('./filezilla/' + inpt2, 'zip', './filezilla/' + inpt2)
                    fz = inpt2 + '.zip'                   
                    f.retrbinary("RETR " + fz, open(fz, 'wb').write)
                    f.delete(fz)

            client_socket.send(message.encode())


            # jika kata kunci SEND maka akan melakukan fungsi send file ke server
            # if message.split()[2] == "SENDALL":
            #     send_file(message.split()[3])
           

        except KeyboardInterrupt:
            print('you left the chat')
            message = str(client_socket.getsockname()) + ' ' + 'closed'
            client_socket.send(message.encode())
            client_socket.close()
            sys.exit(0)
            break