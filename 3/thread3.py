import threading

def worker(num):
    print("worker: " + str(num))

threads = []
for i in range(10):
    t = threading.Thread(target=worker,args=(i,))
    threads.append(t)
    t.start()