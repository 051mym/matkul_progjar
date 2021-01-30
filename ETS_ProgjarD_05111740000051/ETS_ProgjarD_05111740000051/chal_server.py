# import library utama
import socket
import time
import select
import sys

def send_file(filename):
    f = open(filename, "rb")
    data = f.read(1024)
    while(data):
        if( server_socket.sendto( data, client ) ):
            data = f.read(1024)
            time.sleep(0.02) # Give receiver a bit time to save
    f.close()

def recv_file(filename):
    f = open(filename, 'wb')
    while True:
        ready = select.select([server_socket], [], [], 3)
        if ready[0]:
            data, addr = server_socket.recvfrom(1024)
            f.write(data)
        else:
            f.close()
            break

# membuat socket server udp
server_address = ('localhost', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_socket.bind(server_address)

# set yg akan menyimpan client yg terhubung dengan server
set_client_addr = set(())

while True:
    try:
        # recv data yg dikirim client
        data, client_address = server_socket.recvfrom(1024)
        data_msg = data.decode()

        # jika kata kunci adalah connect (client baru connect) maka akan memasukkan client ke set
        # dan mengirim pesan connected... ke client
        if data_msg.split()[2] == "connect":
            server_socket.sendto("connected...".encode(), client_address)
            set_client_addr.add(client_address)
            print(str(client_address) + ' join the chat')
            continue
        # jika kata kunci adalah close (client left chat) maka akan menghapus client pada set
        elif data_msg.split()[2] == "closed":
            set_client_addr.discard(client_address)
            print(str(client_address) + ' left the chat')
            continue
        # jika kata kunci SEND (client kirim file) maka akan menyimpan file pada server
        elif data_msg.split()[2] == "SENDALL":
            recv_file(data_msg.split()[3])
        
        # broadcast message kesemua user yg ada dalam set
        for client in set_client_addr:
            msg_usr = data_msg.split()[:2]
            user = str(client).split()
            # akan mengirim pesan kecuali user yg mengirim
            if msg_usr != user:
                server_socket.sendto(data_msg.encode(), client)
                print('message : ' + str(data_msg) + ' to : ' + str(client))

                # read file dan mengirimkan ke client"
                if data_msg.split()[2] == "SENDALL":
                    send_file(data_msg.split()[3])

    except KeyboardInterrupt:
        print(str(server_socket.getsockname()) + ' has down')
        server_socket.close()
        sys.exit(0)
        break