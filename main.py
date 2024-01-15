###############################################################################################################
#
#                               METAPHONE by Codeiro - ValenArb
#
###############################################################################################################


import time
from multiprocessing import Process, active_children
from multiprocessing.shared_memory import SharedMemory
from libs.Matrix import Matrix
from libs.AudioManager import *
from libs.sub_libs.variables import *
from libs.PhoneBell import ring



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
            play_tone(number.buf[0])
            time.sleep(0.005)
            number.buf[0] = 11

def code_main():
    audio = Process(target=Audio)
    key = SharedMemory(name="Memory", create=False)
    keypress = []
    endtime = time.time() + 10
    while endtime >= time.time():
        keypres = key.buf[0]
        if keypres != 11:
            keypress.append(keypres)
            last = keypres
            while keypres == last:
                keypres = key.buf[0]
    code = ''.join(map(str, keypress))+'.wav'
    value = audio_message(code)
    if value == False:
        code_main()


def welcome():
    audio_welcome()
    options = Process(target=audio_options, name = "Options")
    options.start()
    key = SharedMemory(name="Memory", create=False)
    end_time = time.time() + Max_Timeout_Start_Menu + 10
    j = True
    while j == True:
        keypad = key.buf[0]
        if time.time() >= end_time or key.buf[6+4] == 1:
            j = False
            options.terminate()
            finish()
        elif keypad == 1: #Record message
            j = False
            options.terminate()
            recorder_main()
        elif keypad == 2: #Random message
            options.terminate()
            j = False
            time.sleep(0.5)
            audio_recive()
            time.sleep(0.5)
            audio_message()
            time.sleep(1)
            finish()
        elif keypad == 3: #Code message
            j = False
            options.terminate()
            code_main()
    finish()

def finish(kill = False):
    """Finish all process and play goodbye audio.""" 
    key = SharedMemory(name="Memory", create=False) 
    notkill = ["Keypad", "Inputs", "Movement"]
    if kill == True:
        notkill.append("Finisher")
    if key.buf[4] == 0:
        finishing = Process(target=audio_finish, name= "Finisher")
        finishing.start()
        time.sleep(3)
    for p in active_children():
        if not p.name in notkill:
            print(p.name)
            p.terminate()
    finishing.join()

if __name__ == "__main__":
    keypad = Process(target=start_keypad, name = "Keypad")
    keypad.start()
    time.sleep(1)
    movement = Process(target = ring, name = "Movement")
    hanged = 0
    mem = SharedMemory(name = "Memory", create=False)
    while True:
        if mem.buf[1] == 1:
            if mem.buf[2] == 1:
                if mem.buf[4] == 0 and hanged == 0:
                    tone_dialing(3, 1)
                    welcomer = Process(target=welcome)
                    hanged = 1
                    welcomer.start()
                if mem.buf[4] == 1 and hanged == 1:
                    hanged = 0
                    
                    finish(True)
            else:
                while mem.buf[4] == 0:
                    tone_ool()
        else:
            ... #TODO Code that copies the 'recordings' folder and 'timely.txt' to a pendrive. If 'timely.txt' in pendrive copies it and reboots the system
            
#TODO WHEN FINISHED AND THANKED PLAY OCUPPIED TONE
#TODO GET ALL VARIABLES OF TIME ON A TXT or json or any other way that is apb

