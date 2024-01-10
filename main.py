###############################################################################################################
#
#                               METAPHONE by Codeiro - ValenArb
#
###############################################################################################################


import time
from multiprocessing import Process, active_children
from multiprocessing.shared_memory import SharedMemory
from cogs.Matrix import Matrix
from cogs.Recorder import Recorder
from cogs.Players import *
from cogs.Signals import *
from cogs.Player import Player as Play
import os
import random
from cogs.file import filename

def recordi(timer = 60, recordmore = None):
    a = SharedMemory(name="Memory", create=False)
    j = True
    rec = Recorder()
    print("Started recording")
    play_record()
    start_time = time.time()
    finish_time = start_time + timer
    rec.start()
    if recordmore == None:
        name = filename()
    else:
        name = recordmore
    while j == True:
        f = a.buf[0]
        tiempo = time.time()
        if tiempo >= finish_time:
            j = False
        elif f == 1:
            j = False
    rec.stop()
    rec.save(name)
    return name

def start_keypad():
    """Start a new process to run the keyboard scanner."""
    number = SharedMemory(name="Memory", create=True, size=1000)
    number.buf[0] = 11
    process = Process(target=Matrix)
    process.start()
    print("Keypad process has started correctly!")
    while True:
        time.sleep(0.01)
        if number.buf[0] != 11:
            print(f"{number.buf[0]} has been pressed")
            time.sleep(0.005)
            number.buf[0] = 11

def welcome(tiempo_max = 20):
    welcomer = Process(target=play_welcome, name= "Welcoming")
    welcomer.start()
    key = SharedMemory(name="Memory", create=False)
    start_time = time.time()
    end_time = start_time + tiempo_max
    j = True
    while j == True:
        keypad = key.buf[0]
        tiempo = time.time()
        if tiempo >= end_time or key.buf[6+4] == 1:# Fin de la sesión
            j = False
            welcomer.terminate()
            finish()
        elif keypad == 1:
            j = False
            #random message
            welcomer.terminate()
            time.sleep(0.5)
            randomfile = random.choice(os.listdir("/home/peima/FTP/test/recordings"))
            file = '/home/peima/FTP/test/recordings/' + randomfile
            Play(file)
            print(f"Playing recording N°{randomfile}")
            finish()
        elif keypad == 2:
            j = False
            time.sleep(0.01)
            #select code
            welcomer.terminate()
            coder = Process(target=play_code)
            coder.start()
            keypress = []
            starttime = time.time()
            endtime = starttime + 3
            tiempo = time.time()
            while end_time >= time.time():
                tiempo = time.time()
                keypres = key.buf[0]
                print(keypres)
                if keypres != 11:
                    keypress.append(keypres)
                    time.sleep(0.15)
            code = ''.join(map(str, keypress))+'.wav'
            print(type(code))
            dir = os.listdir('/home/peima/FTP/test/recordings')
            if code in dir:
                coder.terminate()
                Play(dir + '/' + code)
            finish()
            
        elif keypad == 3:
            j = False
            #record message
            welcomer.terminate()
            name = recordi(60)
            play_record_finish()
            starttime = time.time()
            endtime = starttime +3
            while endtime <= time.time():
                if keypad == 1:
                    recordi(60, name)
            filenam = name.split('.')[0]
            digits = [int(d) for d in filenam if d.isdigit()]
            play_message_code()
            for digit in digits:
                play_digits(digit)
                time.sleep(0.2)
            finish()
def finish():
    """Finish all process and play goodbye audio.""" 
    a = key = SharedMemory(name="Memory", create=False) 
    notkill = ["Keypad", "Inputs"]
    if not a.buf[6] == 0:
        play_finish()
    for p in active_children():
        if not p.name in notkill:
            print(p.name)
            
            p.terminate()


if __name__ == "__main__":
    keypad = Process(target=start_keypad, name = "Keypad")
    keypad.start()
    print("keypad")
    time.sleep(1)
    inputs = Process(target=input, args=(4,), name = "Inputs")#23,24]))
    inputs.start()
    print("inputs")
    time.sleep(0.5)
    hanged = 0
    mem = SharedMemory(name = "Memory", create=False)
    while True:
        if mem.buf[6+4] == 0 and hanged == 0:
            welcomer = Process(target=welcome)
            hanged = 1
            welcomer.start()
        if mem.buf[6+4] == 1 and hanged == 1:
            hanged = 0
            finish()
        if mem.buf[6+23] == 1 or mem.buf[6+24] == 1:
            print("movement has been detected!")