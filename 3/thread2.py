import threading

def worker():
    print("saya bekerja")

threads = []
for i in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()