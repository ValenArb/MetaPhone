import gpiozero
from gpiozero import DigitalInputDevice
from multiprocessing.shared_memory import SharedMemory
import time

def input(pins):
    button = SharedMemory(name= "Memory", create= False)
    input = DigitalInputDevice(pin = 4)#for pin in pins]
    while True:
            time.sleep(0.1)
            if input.value == 1:
                button.buf[6+int(str(input.pin)[4:])] = 1
            else:
                button.buf[6+int(str(input.pin)[4:])] = 0