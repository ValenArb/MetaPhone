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
            number.buf[0] = 11

def code_main(retry = True):
    audio_code()
    tones = Process(target = play_tone, name = "Tones")
    key = SharedMemory(name="Memory", create=False)
    keypress = []
    endtime = time.time() + Max_Timeout_Code_Keypress
    tone_beep()
    #TODO preguntar a pablo: Si quiere que cuando se ingrese un codigo. en vez de un tiempo limite, si no se apreta tecla en 1 segundo se toma eso como codigo
    tones.start()
    while endtime >= time.time():
        keypad = key.buf[0]
        last = 11
        if keypad != 11:
            keypress.append(keypad)
            last = keypad
            while keypad == last:
                keypad = key.buf[0]
                key.buf[0] = 11
    tones.terminate()
    code = ''.join(map(str, keypress)) + '.wav'
    print(code)
    a = audio_message(code)    
    if a == False and retry == True:
        code_main(False)
    if retry == False:
        finish() 

def welcome():
    welcome = Process(target=audio_welcome, name = "Options")
    welcome.start()
    key = SharedMemory(name="Memory", create=False)
    end_time = time.time() + Max_Timeout_Start_Menu + 10
    j = True
    while j == True:
        keypad = key.buf[0]
        if time.time() >= end_time or key.buf[11] == 1:
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
    finish()

def finish(ool = False, decorativo= False):
    mem = SharedMemory(name="Memory", create=False) 
    finishing = Process(target=audio_finish, name= "Finisher")
    tonofuera = Process(target=tono_ool, name = "Fuera")
    rotacion = 0
    lista = []
    if ool == True:
        rotacion = 1
    while mem.buf[11] == 0:
        if rotacion == 0:
            rotacion = 1
            finishing.start()
            time.sleep(1)
        else:
            tonofuera.start()
    
def tono_ool():
    while True:
        tone_ool()

def killprocess():
    notkill = ["Keypad", "Inputs", "Movement", "Positions", "Outputs", "Tones"]
    for p in active_children():
        if not p.name in notkill:
            p.terminate()


if __name__ == "__main__":
    mem = SharedMemory(name = "Memory", create=True, size = 1000)
    keypad = Process(target=start_keypad, name = "Keypad")
    keypad.start()
    time.sleep(1)
    movement = Process(target = ring, name = "Movement")
    ins = Process(target = imput, name = "Inputs", args=(5,23,24,11,6))
    outs = Process(target = outbut, name = "Outputs", args=(18,12,27,17))
    position = Process(target = select, name = "Positions")
    # tones.start()
    ins.start()
    outs.start()
    position.start()
    hanged = 1
    time.sleep(2)
    dead = 0
    ta = 0
    while True:
        if mem.buf[40] == 0:
            ta = 0
            # print(mem.buf[11])
            if mem.buf[11] == 0 and hanged == 1:
                dead = 0
                hanged = 0
                j = 0
                i = random.randint(1, 4)
                i = 1 #TODO COMMENT THIS LINE WHEN CODE FINISHED TESTING
                while j <= i:
                    j+=1
                    if mem.buf[11] == 1 or mem.buf[40] != 0:
                        hanged = 1
                        j = 10
                    else:
                        tone_dialing()
                welcomer = Process(target=welcome)
                welcomer.start()
            if mem.buf[11] == 1 and dead == 0:
                dead = 1
                hanged = 1
                killprocess()
        elif mem.buf[40] == 1:
            ta = 1
            tono = Process(target=tono_ool, name= "Trono")
            tono.start()
                
        else:
            killprocess()