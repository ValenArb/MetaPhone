###############################################################################################################
#
#                               METAPHONE by Codeiro - ValenArb
#
###############################################################################################################


import time
from multiprocessing import Process, active_children
from multiprocessing.shared_memory import SharedMemory
from libs.Matrix import Matrix
from libs.Sub_Libs.Recorder import Recorder
from libs.Players import *
from libs.Signals import *
from libs.Sub_Libs.Player import Player as Play
import os
import random
from libs.Sub_Libs.file import filename

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


def random_main():
    time.sleep(0.5)
    randomfile = random.choice(os.listdir("/home/peima/FTP/test/recordings"))
    file = '/home/peima/FTP/test/recordings/' + randomfile
    Play(file)
    return False

def code_main():
    coder = Process(target=play_code)
    coder.start()
    key = SharedMemory(name="Memory", create=False)
    keypress = []
    starttime = time.time()
    endtime = starttime + 3
    tiempo = time.time()
    while endtime >= tiempo:
        tiempo = time.time()
        keypres = key.buf[0]
        if keypres != 11:
            keypress.append(keypres)
            last = keypres
            while keypres == last:
                keypres = key.buf[0]
                print(f"Not mapped {keypres}")
    code = ''.join(map(str, keypress))+'.wav'
    print(code)
    dir = '/home/peima/FTP/test/recordings'
    listdir = os.listdir('/home/peima/FTP/test/recordings')
    if code in listdir:
        coder.terminate()
        Play(dir + '/' + code)
    elif not code in listdir:
        print("the code is incorrect! Please Re do your code")
    return False

def recorder_main():
    name = recordi(60)
    play_record_finish()
    endtime = time.time() +3
    while endtime <= time.time():
        if keypad == 0:
            recordi(60, name)
        filenam = name.split('.')[0]
        digits = [int(d) for d in filenam if d.isdigit()]
        play_message_code()
        for digit in digits:
            play_digits(digit)
            time.sleep(0.2)

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
        if tiempo >= end_time or key.buf[6+4] == 1:
            j = False
            welcomer.terminate()
        elif keypad == 1:
            welcomer.terminate()
            j = random_main()
        elif keypad == 2:
            welcomer.terminate()
            time.sleep(0.02)
            j = code_main()
        elif keypad == 3:
            j = False
            #record message
            welcomer.terminate()
            j = recorder_main()
    finish()

def finish():
    """Finish all process and play goodbye audio.""" 
    a = key = SharedMemory(name="Memory", create=False) 
    notkill = ["Keypad", "Inputs"]
    if a.buf[6+4] == 0:
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
    inputs = Process(target=input, args=(4,), name = "Inputs")#23,24])) #TODO add input for movement sensors
    inputs.start()
    print("inputs")
    hanged = 0
    mem = SharedMemory(name = "Memory", create=False)
    while True:
        if mem.buf[6+4] == 0 and hanged == 0:
            time.sleep(1) #FIXME set to 5-10 secons
            welcomer = Process(target=welcome) #TODO change the welcome. When started 5 seconds of cupaid tone
            hanged = 1
            welcomer.start()
        if mem.buf[6+4] == 1 and hanged == 1:
            hanged = 0
            finish()
        if mem.buf[6+23] == 1 or mem.buf[6+24] == 1:
            print("movement has been detected!")
            
#TODO SEARCH OCUUPIED TONE
#TODO SEARCH OUT OF LINE TONE
#TODO SEARCH CALLING LINE TONE
#TODO WHEN FINISHED AND THANKED PLAY OCUPPIED TONE
#TODO DURING DAYTIME NOT WORK
#TODO GET ALL VARIABLES OF TIME ON A TXT or json or any other way that is apb

