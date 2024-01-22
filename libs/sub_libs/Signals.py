import gpiozero
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from multiprocessing.shared_memory import SharedMemory
import time

def imput(pins):
    mem = SharedMemory(name= "Memory", create= False)
    for pin in pins:
        input = DigitalInputDevice(pin=pin)
        if input.value == 1:
            mem.buf[pin] = 1
        else:
            mem.buf[pin] = 0
                

def output(pins: list, status: bool):
    outs = [DigitalOutputDevice(pin = pin) for pin in pins]
    for out in outs:
        if status == True:
            out.on()
        else:
            out.off()    