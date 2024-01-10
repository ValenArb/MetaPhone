import gpiozero
from gpiozero import DigitalInputDevice
from multiprocessing.shared_memory import SharedMemory
import time

def input(pins):
    button = SharedMemory(name= "Memory", create= False)
    for pin in pins:
        inputs = [DigitalInputDevice(pin = pin)for pin in pins]
    for input in inputs:
        while True:
            time.sleep(0.1)
            if input.value == True:
                button.buf[6+int(inputs.pin)] = 1
            else:
                button.buf[6+int(inputs.pin)] = 0