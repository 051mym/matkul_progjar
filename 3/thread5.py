import threading
import logging

logging.basicConfig(level=logging.DEBUG, format="%(threadName)s > %(message)s",)

class Mythread(threading.Thread):
    def __init__(self,num):
        threading.Thread.__init__(self)
        self.num = num
    def run(self):
        logging.debug(str(self.num) + ' running')

for i in range(5):
    t = Mythread(i)
    t.start()