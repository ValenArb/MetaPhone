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
# from libs.sub_libs.Player import Player as Play
import os
from libs.PhoneBell import ring
import random



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
            print(f"{number.buf[0]} has been pressed")
            time.sleep(0.005)
            number.buf[0] = 11

def code_main(re_play= False):
    if re_play == False:
        coder = Process(target=play_code)
        coder.start()
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
                print(f"Not mapped {keypres}")
    code = ''.join(map(str, keypress))+'.wav'
    correct = play_message(code)
    if correct == False:
        code_main()


def welcome(tiempo_max = 20):
    welcomer = Process(target=play_welcome, name= "Welcoming")
    welcomer.start()
    key = SharedMemory(name="Memory", create=False)
    end_time = time.time() + tiempo_max
    j = True
    while j == True:
        keypad = key.buf[0]
        if time.time() >= end_time or key.buf[6+4] == 1:
            j = False
            welcomer.terminate()
        elif keypad == 1:
            welcomer.terminate()
            j = play_message
        elif keypad == 2:
            welcomer.terminate()
            time.sleep(0.02)
            j = code_main()
        elif keypad == 3:
            j = False
            welcomer.terminate()
            j = recorder_main()
    finish()

def finish():
    """Finish all process and play goodbye audio.""" 
    a = key = SharedMemory(name="Memory", create=False) 
    notkill = ["Keypad", "Inputs", "Movement"]
    if a.buf[6+4] == 0:
        play_finish()
    for p in active_children():
        if not p.name in notkill:
            print(p.name)
            
            p.terminate()

if __name__ == "__main__":
    keypad = Process(target=start_keypad, name = "Keypad")
    keypad.start()
    time.sleep(1)
    movement = Process(target = ring, name = "Movement")
    hanged = 0
    mem = SharedMemory(name = "Memory", create=False)
    while True:
        if mem.buf[6+4] == 0 and hanged == 0:
            time.sleep(5)
            welcomer = Process(target=welcome)
            hanged = 1
            welcomer.start()
        if mem.buf[6+4] == 1 and hanged == 1:
            hanged = 0
            finish()
            
#TODO WHEN FINISHED AND THANKED PLAY OCUPPIED TONE
#TODO DURING DAYTIME NOT WORK
#TODO GET ALL VARIABLES OF TIME ON A TXT or json or any other way that is apb

