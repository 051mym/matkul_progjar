import threading
import datetime

class ThreadClass(threading.Thread):
    def run(self):
        now = datetime.datetime.now()
        print(self.getName()+ " Hello at " + str(now)+"\n")

for i in range(10):
    t = ThreadClass()
    t.start() 