#######
#FILE 3: performance.py
#######
import time

class FpsMeter:
    def __init__(self):
        self.boundary = time.time()
        self.count = 0;
        self.returned = 0
        
    def go(self):
        self.count = self.count + 1
        if time.time() - self.boundary > 1:
            self.boundary = time.time()
            self.returned = self.count
            self.count = 0
            
        return self.returned
