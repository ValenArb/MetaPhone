from multiprocessing.shared_memory import SharedMemory
from multiprocessing import Process
import time
from libs.sub_libs.Signals import *

def ring():
    mem = SharedMemory(name= "Memory", create = False)
    while True:
        sensor1 = mem.buf[23]
        sensor2 = mem.buf[24]
        if sensor1 == 1 or sensor2 == 1:
            cycle = 0
            while cycle < 5:
                output(18, True)
                if mem.buf[11] == 0:
                    cycle == 60
                else:
                    time.sleep(3)
                    output(18, False)
                    time.sleep(1)
                    cycle += 1
        if mem.buf[11] == 1:
            output(17, True)
        else:
            output(17, False)
                    
def select():
    mem = SharedMemory(name="Memory", create = False)
    while True:
        poscion1 = mem.buf[6]
        poscion2 = mem.buf[5]
        if poscion1 == 0 and poscion2 == 0:
            mem.buf[40] = 1
            output(17, False)
            output(27, True)
        elif poscion1 == 1:
            mem.buf[40] = 0
            output(17, True)
            output(27, False)
        elif poscion2 == 1:
            mem.buf[40] = 2
            output(17, True)
            output(27, True)