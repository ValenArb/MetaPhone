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
    endtime = time.time() + Max_Timeout_Code_Keypress + 2
    tone_beep()
    tones.start()
    while endtime >= time.time():
        keypad = key.buf[0]
        last = 11
        if keypad != 11:
            keypress.append(keypad)
            last = keypad
            endtime = endtime + Max_Timeout_Code_Keypress
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
    end_time = time.time() + Max_Timeout_Start_Menu + 20
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

def finish():
    audio_finish()
    tono_ool()
    
def tono_ool():
    while True:
        tone_ool()

def killprocess():
    mem = SharedMemory(name = "Memory")
    while mem.buf[143] == 1:
        ...
    if mem.buf [143] == 0:
        notkill = ["Keypad", "Inputs", "Campanilla", "Positions", "Outputs"]
        for p in active_children():
            if not p.name in notkill:
                p.terminate()


if __name__ == "__main__":
    mem = SharedMemory(name = "Memory", create=True, size = 1000)
    keypad = Process(target=start_keypad, name = "Keypad")
    keypad.start()
    time.sleep(1)
    movement = Process(target = ring, name = "Campanilla")
    ins = Process(target = imput, name = "Inputs", args=(5,23,24,11,6))
    outs = Process(target = outbut, name = "Outputs", args=(18,12,27,17))
    position = Process(target = select, name = "Positions")
    movement.start()
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
            if mem.buf[11] == 0 and hanged == 1:
                hanged = 0
                i = random.randint(1, 2)
                # i = 1 #TODO COMMENT THIS LINE WHEN CODE FINISHED TESTING
                if mem.buf[200] == 1:
                    time.sleep(1)
                    tone_beep()
                if mem.buf[11] == 1 or mem.buf[40] != 0:
                    hanged = 1
                else:
                    dialer = Process(target=tone_dialing, args= i)
                    dialer.start()
                welcomer = Process(target=welcome)
                welcomer.start()
            if mem.buf[11] == 1:
                hanged = 1
                killprocess()
        elif mem.buf[40] == 1:
            ta = 1
            tono = Process(target=tono_ool, name= "Trono")
            tono.start()
                
        else:
            killprocess()
            
#TODO AL TERMINAR EL AUDIO FIN GRABAR (EL QUE TE DICE 9 PARA REGRABAR) AGREGAR UN BEEP // Arreglado
#TODO NO ANDA TONO FUERA DE LINEA? NO SE PORQUE // Arreglado
#TODO ACTUALIZAR LA TARJETA DE MEMORIA DE 32GB
#TODO CAMBIAR A 5 MINUTOS LA CAMPANILLA
#TODO VER SI TIENE ARREGLO EL CICLO DE LA CAMPANA (QUE SI ATENDES EN EL MOMENTO QUE NO VERIFICA SI LEVANTASTE ) // No tiene solucion facil
#TODO PROBAR CON MUCHA GENTE
#TODO REDUCIR TIEMPO DE ESPERA PARA INGRESAR CODIGO // Arreglado y mejorado
