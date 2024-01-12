from multiprocessing.shared_memory import SharedMemory
from multiprocessing import Process
import time
from libs.sub_libs.Signals import *

def ring():
    mem = SharedMemory(name= "Memory", create = False)
    movement = Process(target = input, args= [23, 24], name= "Inputs")
    movement.start()
    while True:
        time.sleep(5)
        sensor1 = mem.buf[23]
        sensor2 = mem.buf[24]
        if sensor1 == 1 or sensor2 == 1:
            output(9, True)
            time.sleep(20)
            output(9, False)
        else:
            output(9, False)