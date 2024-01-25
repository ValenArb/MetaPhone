###############################################################################################################
#
#                               METAPHONE by Codeiro - ValenArb
#
###############################################################################################################


import time
from multiprocessing import Process, active_children
import random
from multiprocessing.shared_memory import SharedMemory
from libs.Matrix import Matrix
from libs.AudioManager import *
from variables import *
from libs.PhoneBell import *
from libs.sub_libs.Signals import *

def start_keypad():
    """Start a new process to run the keyboard scanner."""
    number = SharedMemory(name="Memory", create=False)
    number.buf[0] = 11
    process = Process(target=Matrix)
    process.start()
    print("Keypad process has started correctly!")
    while True:
        time.sleep(0.01)
        if number.buf[0] != 11:
            play_tone(number.buf[0])
            time.sleep(0.0005)
            number.buf[0] = 11

def code_main(retry = True):
    audio_code()
    key = SharedMemory(name="Memory", create=False)
    keypress = []
    endtime = time.time() + Max_Timeout_Code_Keypress
    tone_beep()
    while endtime >= time.time():
        keypad = key.buf[0]
        last = 11
        if keypad != 11:
            keypress.append(keypad)
            last = keypad
            while keypad == last:
                keypad = key.buf[0]
                key.buf[0] = 11
    code = ''.join(map(str, keypress)) + '.wav'
    print(code)
    a = audio_message(code)    
    if a == False and retry == True:
        code_main(False)
    if retry == False:
        finish(False) 

def welcome():
    welcome = Process(target=audio_welcome, name = "Options")
    welcome.start()
    key = SharedMemory(name="Memory", create=False)
    end_time = time.time() + Max_Timeout_Start_Menu + 10
    j = True
    while j == True:
        keypad = key.buf[0]
        if time.time() >= end_time or key.buf[6] == 1:
            j = False
            try:
                welcome.terminate()
            except:
                continue
        elif keypad == Send_Message_Key: #Record message
            j = False
            try:
                welcome.terminate()
            except:
                continue
            recorder_main()
        elif keypad == Random_Message_Key: #Random message
            j = False
            try:
                welcome.terminate()
            except:
                continue
            time.sleep(0.5)
            audio_recive()
            time.sleep(0.5)
            audio_message()
            time.sleep(1)
        elif keypad == Code_Message_Key: #Code message
            j = False
            try:
                welcome.terminate() 
            except:
                continue
            code_main()
    finish(False)

def finish(kill = True):
    """Finish all process and play goodbye audio.""" 
    key = SharedMemory(name="Memory", create=False) 
    notkill = ["Keypad", "Inputs", "Movement", "Positions"]
    finishing = Process(target=audio_finish, name= "Finisher")
    if key.buf[6] == 0:
        if kill == False:
            notkill.append("Finisher")
        finishing.start()
    for p in active_children():
        if not p.name in notkill:
            print(p.name)
            p.terminate()
    if kill == False:
        try:
            finishing.join()
        except: 
            ...
    while key.buf[6] == 0:
        # rotations += 1
        # if rotations != 4:
        #     tone_busy()
        #     time.sleep(1)
        # else:
            tone_ool()
        
        

if __name__ == "__main__":
    mem = SharedMemory(name = "Memory", create=True, size = 1000)
    keypad = Process(target=start_keypad, name = "Keypad")
    keypad.start()
    time.sleep(1)
    movement = Process(target = ring, name = "Movement")
    hangup = Process(target = imput, name = "Inputs", args=(6,23,24,11,5))
    position = Process(target = select, name = "Positions")
    hangup.start()
    position.start()
    hanged = 0
    mem.buf[40] = 1 #position of X
    mem.buf[6] = 1
    while True:
        if mem.buf[40] == 0:
            if mem.buf[6] == 0 and hanged == 0:
                j = 0
                i = random.randint(2, 5)
                i = 0 #TODO COMMENT THIS LINE WHEN CODE FINISHED TESTING
                while j <= i:
                    j+=1
                    if mem.buf[6] == 1:
                        break
                    else:
                        tone_dialing()
                        time.sleep(0.5) 
                welcomer = Process(target=welcome)
                hanged = 1
                welcomer.start()
            if mem.buf[6] == 1 and hanged == 1:
                hanged = 0
                finish(True)
        elif mem.buf[40] == 0:
            while mem.buf[6] == 0:
                tone_ool()
        else:
            ...