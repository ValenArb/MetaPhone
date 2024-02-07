from multiprocessing.shared_memory import SharedMemory
from multiprocessing import Process
import time
from libs.sub_libs.Signals import *

def ring():
    mem = SharedMemory(name= "Memory", create = False)
    j = 0
    time.sleep(10)
    cycle = 0
    start_in = 0
    while True:
        if mem.buf[40] == 0:
            print("1")
            if mem.buf[11] == 0:
                start_in = time.time() + 300
                cycle = 0
            else:
                while start_in >= time.time():
                    if mem.buf[11]== 0:
                        start_in = 1000000000000000000000000000000000000000000000000000000000000
                    print(f"""
                          Iniciamos: {start_in}
                          Tiempo: {time.time()}
                          """)
                    ...
            while cycle <= 5 and mem.buf[11] == 1:
                print(4)
                output(12, True)
                time.sleep(1.5)
                output(12, False)
                time.sleep(3)
                cycle += 1
            if cycle >= 5:
                print(5)
                cycle = 0
                start_in = time.time() + 300
        else:
            time.sleep(0.5)
        

def select():
    mem = SharedMemory(name="Memory", create = False)
    a = 0
    while True:
        poscion1 = mem.buf[6]
        poscion2 = mem.buf[5]
        if poscion1 == 0:
            # print("Estado 1")
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