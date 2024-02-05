import gpiozero
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from multiprocessing.shared_memory import SharedMemory
import time

def imput(pin1 = None,pin2 = None,pin3 = None,pin4 = None,pin5 = None,pin6 = None,pin7 = None):
    pins = [pin1, pin2, pin3, pin4, pin5, pin6, pin7]
    j= True
    inputs = []
    while j == True:
        if None in pins:
            pins.remove(None)            
        else:
            j = False
    mem = SharedMemory(name= "Memory", create= False)
    for pin in pins:
        input = DigitalInputDevice(pin=pin)
        inputs.append(input)
    try:
        while True:
            for input in inputs:
                pin = input.pin.number
                if input.value == 1:
                    mem.buf[pin] = 1
                else:
                    mem.buf[pin] = 0
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        for i in inputs:
            i.close()

def outbut(pin1 = None,pin2 = None,pin3 = None,pin4 = None,pin5 = None,pin6 = None,pin7 = None):
    pins = [pin1, pin2, pin3, pin4, pin5, pin6, pin7]
    j = True
    while j == True:
        if None in pins:
            pins.remove(None)
        else:
            j = False
    outputs = []
    mem = SharedMemory(name="Memory", create= False)
    for pin in pins:
        outputed = DigitalOutputDevice(pin = pin)
        outputs.append(outputed)
    try:
        while True:
            for i in outputs:
                pin = i.pin.number
                value = mem.buf[int(pin)]
                if value == 1:
                    try:
                        i.on()
                    except:
                        ...
                else:
                    try:
                        i.off()
                    except:
                        ...
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        for i in outputs:
            i.close()
def output(pin: int, status: bool):
    mem = SharedMemory(name="Memory", create= False)
    if status == True:
        mem.buf[pin] = 1
    else:
        mem.buf[pin] = 0
    return