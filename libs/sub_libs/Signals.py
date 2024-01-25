import gpiozero
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from multiprocessing.shared_memory import SharedMemory
import time

def imput(pin1 = None,pin2 = None,pin3 = None,pin4 = None,pin5 = None,pin6 = None,pin7 = None):
    pins = [pin1, pin2, pin3, pin4, pin5, pin6, pin7]
    j= True
    while j == True:
        if None in pins:
            pins.remove(None)
        else:
            j = False
    mem = SharedMemory(name= "Memory", create= False)
    for pin in pins:
        input = DigitalInputDevice(pin=pin)
        if input.value == 1:
            mem.buf[pin] = 1
        else:
            mem.buf[pin] = 0
                

def output(pin, status: bool):
    out = DigitalOutputDevice(pin = pin)
    if status == True:
        try:
            out.on()    
        except:
            ...
    else:
        try:            
            out.off() 
        except:
            ...
    return