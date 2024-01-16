import gpiozero
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from multiprocessing.shared_memory import SharedMemory
import time

def imput(pin= 4):
    mem = SharedMemory(name= "Memory", create= False)
    input = DigitalInputDevice(4)
    while True:
            time.sleep(0.1)
            if input.value == 1:
                mem.buf[4] = 1
            else:
                mem.buf[4] = 0
                

def output(pins: list, status: bool):
    outs = [DigitalOutputDevice(pin = pin) for pin in pins]
    for out in outs:
        if status == True:
            out.on()
        else:
            out.off()    