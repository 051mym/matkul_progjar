import socket
import select
import queue
from threading import Thread
from time import sleep
from random import randint
import sys

class ProcessThread(Thread):
    def __init__(self):
        super(ProcessThread, self).__init__()
        self.running = True
        self.q = queue.Queue()

    def add(self, data):
        self.q.put(data)

    def stop(self):
        self.running = False

def run(self):
    q = self.q
    while self.running:
        try:
            # block for 1 second only:
            value = q.get(block=True, timeout=1)
            process(value)
        except Queue.Empty:
            sys.stdout.write('.')
            sys.stdout.flush()
    if not q.empty():
        print("Elements left in the queue:")
        while not q.empty():
            print(q.get())

t = ProcessThread()
t.start()

def process(value, client):
    print(value)
    log = 'log.txt'
    f= open("log.txt","a+")
    f.write("data = " + str(value))
    f.close() 
    client.send(value.encode())
    sleep(randint(1,5)) # emulating processing time

def main():
    s = socket.socket() # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 5005 # Reserve a port for your service.
    s.bind(("localhost", port)) # Bind to the port
    print("Listening on host {p}...".format(p=host))

    s.listen(5) # Now wait for client connection.
    while True:
        try:
            client, addr = s.accept()
            ready = select.select([client,],[], [],2)
            if ready[0]:
                data = client.recv(4096).decode()
                print(data)
                process(data,client)
                
                t.add(data)

        except KeyboardInterrupt:
            # print
            print("Stop.")
            break
        except (socket.error):
            print("Socket error! %s" % "msg")
            break
    #
    cleanup()

def cleanup():
    t.stop()
    t.join()

if __name__ == "__main__":
    main()