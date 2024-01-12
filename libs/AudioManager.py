from libs.sub_libs.Player import Player as Play
from multiprocessing.shared_memory import SharedMemory
from libs.sub_libs.Recorder import Recorder
from libs.sub_libs.file import filename
import time
import random
import os

def tone_dialing(times: int, space: int = 3):
    """Plays the dialing tone
    Args:
        times (int): Amount of times dialing will be played
        space (int, optional): time in seconds between tones. Defaults to 3.
    """
    while times != 0:
        dir = '/home/peima/FTP/test/audio/tone/calling.wav'
        Play(dir) 
        times -= 1
        time.sleep(space)

def tone_beep(times: int, space: int = 1):
    """Play the beep tone

    Args:
        times (int): Amout of times the tone will be played
        space (int, optional): time in seconds between tones. Defaults to 1.
    """
    while times != 0:
        dir = '/home/peima/FTP/test/audio/tone/beep.wav'
        Play(dir)
        times -= 1
        time.sleep(space)

def audio_welcome():
    """Plays the welcome audio"""
    dir = '/home/peima/FTP/test/audio/welcome.wav'
    Play(dir)
    #Audio 0

def audio_options(space:int = 1):
    """Plays the 3 audios related to options

    Args:
        space (int, optional): Time in seconds between audios. Defaults to 1.
    """ 
    optionlist = ['send.wav','recieve.wav', 'code.wav']
    for option in optionlist:
        dir = '/home/peima/FTP/test/audio/options/'
        Play(dir)
        time.sleep(space)
    #Audio 1, 2 y 3

def play_record(re = False):
    """Plays the record message, if 're' set to true will only say that you can record after the tone

    Args:
        re (bool, optional): Option to re record audio. If True, will play the re record audio. Defaults to False.
    """
    if re == False:
        dir = '/home/peima/FTP/test/audio/Record.wav'
        #Audio 1.1
    else:
        dir = '/home/peima/FTP/test/audio/Record.wav'
        #Audio 1.1.1
    Play(dir)
    
def play_re_record():
    
    ...
    
def play_record_finish():
    dir = '/home/peima/FTP/test/audio/Code.wav'
    Play(dir) #TODO RECORD Your code message (Your code is)
    
def play_digits(digits: list):
    dirs = ['cero.wav', 'uno.wav', 'dos.wav', 'tres.wav', 'cuatro.wav', 'cinco.wav', 'seis.wav', 'siete.wav','ocho.wav', 'nueve.wav']
    odir = '/home/peima/FTP/test/audio/' 
    # odir = 'C:/Users/Peima VM/Desktop/Metaphone/audio/'
    for digit in digits:
        dir = odir + dirs[digit]
        Play(dir)



def play_message_code():
    dir = '/home/peima/FTP/test/audio/Message_code.wav'
    Play(dir)
    
def play_tone(number):
    dirs = ['tone0', 'tone1', 'tone2', 'tone3', 'tone4', 'tone5', 'tone6', 'tone7', 'tone8', 'tone9']
    odir = '/home/peima/FTP/test/audio/tone/'  
    dir = odir + dir[number]
    Play(dir)
    return
    
def play_message(code = None):
    dir = '/home/peima/FTP/test/recordings'
    listdir = os.listdir('/home/peima/FTP/test/recordings')
    if code == None:
        print("A random audio will be played after the beep") #TODO Audio for when a random audio will be played
        code = random.choice(listdir)
    elif not code in listdir:
        print("The code is incorrect") #TODO Audio for when code is incorrect
        return False
    Play(code)
    return True



def record(timer = 60, recordmore = None):
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

def recorder_main():
    name = record(60)
    key = SharedMemory(name="Memory", create=False)
    play_record_finish()
    endtime = time.time() +3
    while endtime <= time.time():
        keypad = key.buf[0]
        if keypad == 0:
            record(60, name)
        filenam = name.split('.')[0]
        digits = [int(d) for d in filenam if d.isdigit()]
        play_message_code()
        for digit in digits:
            play_digits(digit)
            time.sleep(0.2)