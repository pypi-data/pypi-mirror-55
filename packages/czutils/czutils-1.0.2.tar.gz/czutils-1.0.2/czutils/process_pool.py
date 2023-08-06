# --*-- encoding = utf8 --*--
#!/usr/bin/env python3

import multiprocessing
from czutils.singleton_metaclass import SingletonMetaClass

class ProcessPool(metaclass=SingletonMetaClass):
    def __init__(self, process_num=5):
        self.queue = multiprocessing.Queue()
        self.processes = []
        for i in range(process_num):
            process = multiprocessing.Process(target=self._process)
            self.processes.append(process)
            process.start()

    def _process(self):
        while True:
            task = self.queue.get()
            if task[0] == 'q':
                return

            if task[0] == 'c':
                task[1][0](task[1][1])

    def process(self, target):
        print(target)
        self.queue.put(('c', target))
        
    def stop(self):
        for i in range(len(self.processes)):
            self.queue.put(('q', ''))
        for p in self.processes:
            p.join()



