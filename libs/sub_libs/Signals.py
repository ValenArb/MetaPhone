import gpiozero
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from multiprocessing.shared_memory import SharedMemory
import time

def input(pins: list):
    mem = SharedMemory(name= "Memory", create= False)
    inputs = [DigitalInputDevice(pin = pin) for pin in pins]
    while True:
        for input in inputs:
            time.sleep(0.1)
            if input.value == 1:
                mem.buf[int(str(input.pin)[4:])] = 1
            else:
                mem.buf[int(str(input.pin)[4:])] = 0
                

def output(pins: list, status: bool):
    outs = [DigitalOutputDevice(pin = pin) for pin in pins]
    for out in outs:
        if status == True:
            out.on()
        else:
            out.off()    