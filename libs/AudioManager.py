from libs.sub_libs.Player import Player as Play
from multiprocessing.shared_memory import SharedMemory
from libs.sub_libs.Recorder import Recorder
from libs.sub_libs.file import filename
from variables import *
import time
import random
import os

def tone_dialing():
    """Plays the dialing tone"""
    dir = '/home/FuegoAustral/Metaphone/Audios/tone/dial.wav'
    Play(dir) 
    return

def tone_beep():
    """Play the beep tone"""
    dir = '/home/FuegoAustral/Metaphone/Audios/tone/beep.wav'
    Play(dir)

def tone_ool():
    dir = '/home/FuegoAustral/Metaphone/Audios/tone/off-hook.wav'
    Play(dir)
    return

def tone_busy():
    dir = '/home/FuegoAustral/Metaphone/Audios/tone/busy.wav'
    Play(dir)
    return

def audio_welcome():
    """Plays the welcome audio"""
    dir = '/home/FuegoAustral/Metaphone/Audios/General/Bienvenida.wav'
    Play(dir)
    audio_options()
    return

def audio_options(space:int = 1):
    """Plays the 3 audios related to options

    Args:
        space (int, optional): Time in seconds between audios. Defaults to 1.
    """ 
    optionlist = ['Send.wav','Recieve.wav', 'Code.wav']
    for option in optionlist:
        dir = '/home/FuegoAustral/Metaphone/Audios/Opciones/'
        Play(dir + option)
        time.sleep(space)
    return

def audio_record(re = False):
    """Plays the record message, if 're' set to true will only say that you can record after the tone

    Args:
        re (bool, optional): Option to re record audio. If True, will play the re record audio. Defaults to False.
    """
    if re == False:
        dir = '/home/FuegoAustral/Metaphone/Audios/Preguntas'
        file = random.choice(os.listdir(dir))
        dir = dir + '/' + file
    dir2 = '/home/FuegoAustral/Metaphone/Audios/General/Grabacion.wav'
    Play(dir)
    time.sleep(0.5)
    Play(dir2)
    return

def audio_re_record():
    """Plays the re record message"""
    dir = '/home/FuegoAustral/Metaphone/Audios/General/FinGrabar.wav'
    Play(dir) 
    return

def audio_record_finish():
    """Plays the recording finished message"""
    dir = '/home/FuegoAustral/Metaphone/Audios/General/Enviado.wav'
    Play(dir) 
    return

def play_digits(digits: list):
    dirs = ['cero.wav', 'uno.wav', 'dos.wav', 'tres.wav', 'cuatro.wav', 'cinco.wav', 'seis.wav', 'siete.wav','ocho.wav', 'nueve.wav']
    odir = '/home/FuegoAustral/Metaphone/Audios/Numeros/'
    for digit in digits:
        dir = odir + dirs[int(digit)]
        Play(dir)
        time.sleep(0.5)


def audio_recive():
    """Plays the recive message audio"""
    dir = '/home/FuegoAustral/Metaphone/Audios/General/Recibir.wav'
    Play(dir)
    return
    
def play_tone(number: int):
    dirs = ['tone0.wav', 'tone1.wav', 'tone2.wav', 'tone3.wav', 'tone4.wav', 'tone5.wav', 'tone6.wav', 'tone7.wav', 'tone8.wav', 'tone9.wav']
    odir = '/home/FuegoAustral/Metaphone/Audioss/tone/number/'  
    dir = odir + dirs[number]
    Play(dir)
    return
    
def audio_message(code: str = None):
    """Plays a message, if code not given will play random, otherwise the code, if it doesn't exist returns false

    Args:
        code (str, optional): Code to be played. Defaults to None.

    Returns:
        False: The code given doesn't exist
    """
    notfound = '/home/FuegoAustral/Metaphone/Audios/General/NoCode.wav'
    dir = '/home/peima/FTP/test/recordings'
    listdir = os.listdir(dir)
    if code == None:
        code = random.choice(listdir)
    else:
        if not code in listdir:
            print(code)
            print(listdir)
            Play(notfound)
            return False
    tone_beep()
    time.sleep(0.1)
    Play(dir + '/' + code)
    return True

def audio_code():
    dir = '/home/FuegoAustral/Metaphone/Audios/General/Ingrese.wav' 
    Play(dir) 
    return    

def audio_finish():
    """Plays the finishing audio"""
    dir = '/home/FuegoAustral/Metaphone/Audios/General/Salir.wav'
    Play(dir) 
    return


def record(max_time = 60, name: str = None):
    a = SharedMemory(name="Memory", create=False)
    j = True
    rec = Recorder()
    tone_beep()
    rec.start()
    if name == None:
        name = filename()
    finish_time = time.time() + max_time
    while j == True:
        f = a.buf[0]
        if time.time() >= finish_time:
            j = False
        elif f == Stop_Record_Key:
            j = False
        elif a.buf[4] == 1:
            rec.stop()
            rec.save(str(name))
    rec.stop()
    rec.save(str(name))
    return name

def recorder_main(again = False, name = None):
    audio_record(again)
    time.sleep(0.5)
    key = SharedMemory(name="Memory", create=False)
    name = record(max_time=Max_Record_Time, name= name)
    if again == False:
        j = True
        audio_re_record()
        endtime = time.time() + Max_Timeout_Record_Menu
        while j == True:
            if key.buf[0] == Retry_Record_Key:
                j = False
                recorder_main(again = True, name = name)
            elif endtime >= time.time():
                j = False
        time.sleep(0.5)
        audio_record_finish()
        time.sleep(0.5)
        print(name)
        play_digits(list(str(name)))
        time.sleep(1)
        audio_recive()
        time.sleep(0.5)
        audio_message()