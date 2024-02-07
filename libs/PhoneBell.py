from multiprocessing.shared_memory import SharedMemory
from multiprocessing import Process
import time
from libs.sub_libs.Signals import *
from variables import *

def ring():
    mem = SharedMemory(name= "Memory", create = False)
    j = 0
    cycle = 0
    start_at = 0
    while True:
        time.sleep(1)
        if mem.buf[40] == 0:
            if mem.buf[11] == 1:
                cycle = 0
                while start_at > time.time():
                    mem.buf[200] = 0
                    time.sleep(1)
                    print(f"Tiempo restante: {round(start_at-time.time())} s ")
                    if mem.buf[11] == 0:
                        cycle = 300
                        start_at = 0
                    elif not mem.buf[40] == 0:
                        cycle = 300
                        start_at = 0
                while cycle < 5:
                    mem.buf[200] = 1
                    if mem.buf[11] == 0:
                        cycle = 300
                        time.sleep(0.5)
                        mem.buf[200] = 0
                        break
                    if mem.buf[11] == 1:
                        output(12, True)
                        time.sleep(1.5)
                        output(12, False)
                        time.sleep(3)
                        cycle += 1
                start_at = time.time() + Sleep_Ring_Sound
            if mem.buf[11] == 0:
                start_at = time.time() + Sleep_Ring_Sound
        else:
            start_at = time.time() + Sleep_Ring_Sound

def select():
    mem = SharedMemory(name="Memory", create = False)
    a = 0
    while True:
        poscion1 = mem.buf[6]
        poscion2 = mem.buf[5]
        if poscion1 == 0:
            mem.buf[40] = 0
            if a == 0:
                output(17, False)
                output(27, False)
                a = 1
        elif poscion2 == 0:
            a = 0
            mem.buf[40] = 1
            output(17, True)
            output(27, False)
        else: 
            a = 0
            mem.buf[40] = 2
            output(17, True)
            output(27, True)