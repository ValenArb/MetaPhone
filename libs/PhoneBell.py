from multiprocessing.shared_memory import SharedMemory
from multiprocessing import Process
import time
from libs.sub_libs.Signals import *

def ring():
    mem = SharedMemory(name= "Memory", create = False)
    time.sleep(10)
    while True:
        cycle = 0
        while cycle < 5:
                output(18, True)
                if mem.buf[11] == 1:
                    cycle == 60
                else:
                    time.sleep(1,5)
                    output(18, False)
                    time.sleep(3)
                    cycle += 1
        time.sleep(600)
                    
def select():
    mem = SharedMemory(name="Memory", create = False)
    a = 0
    while True:
        poscion1 = mem.buf[6]
        poscion2 = mem.buf[5]
        if poscion1 == 0:
            # print("Estado 1")
            if mem.buf[0] != 11:
                output(17, True)
                time.sleep(0.5)
                output(17, False)
            mem.buf[40] = 0
            if a == 0:
                output(17, False)
                output(27, False)
                a = 1
        elif poscion2 == 0:
            # print("Estado 2")
            a = 0
            mem.buf[40] = 1
            output(17, True)
            output(27, False)
        else: 
            a = 0
            mem.buf[40] = 2
            # print("Estado centrico")
            output(17, True)
            output(27, True)