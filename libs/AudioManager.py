from libs.sub_libs.Player import Player as Play
from multiprocessing.shared_memory import SharedMemory
from libs.sub_libs.Recorder import Recorder
from libs.sub_libs.file import filename
from libs.sub_libs.variables import *
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
        dir = '/home/peima/FTP/test/audio/tone/dial.wav'
        Play(dir) 
        times -= 1
        time.sleep(space)
    return

def tone_beep(times: int = 1, space: int = 1):
    """Play the beep tone

    Args:
        times (int): Amout of times the tone will be played
        space (int, optional): time in seconds between tones. Defaults to 1.
    """
    dir = '/home/peima/FTP/test/audio/tone/beep.wav'
    if not times == 1:
        while times != 0:
            Play(dir)
            times -= 1
            time.sleep(space)
    else:
        Play(dir)
    return

def tone_ool():
    dir = '/home/peima/FTP/test/audio/tone/off-hook.wav'
    Play(dir)
    return

def tone_busy():
    dir = '/home/peima/FTP/test/audio/tone/busy.wav'
    Play(dir)
    return

def audio_welcome():
    """Plays the welcome audio"""
    dir = '/home/peima/FTP/test/audio/general/0.wav'
    Play(dir)
    return

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
    return

def audio_record(re = False):
    """Plays the record message, if 're' set to true will only say that you can record after the tone

    Args:
        re (bool, optional): Option to re record audio. If True, will play the re record audio. Defaults to False.
    """
    if re == False:
        dir = '/home/peima/FTP/test/audio/options'
        file = random.choice(os.listdir(dir))
        dir = dir + '/' + file
    dir2 = '/home/peima/FTP/test/audio/general/1-1.wav'
    Play(dir)
    time.sleep(0.5)
    Play(dir2)
    return

def audio_re_record():
    """Plays the re record message"""
    dir = '/home/peima/FTP/test/audio/general/1-1-1.wav'
    Play(dir) 
    return

def audio_record_finish():
    """Plays the recording finished message"""
    dir = '/home/peima/FTP/test/audio/general/1-2.wav'
    Play(dir) 
    return

def play_digits(digits: list):
    dirs = ['cero.wav', 'uno.wav', 'dos.wav', 'tres.wav', 'cuatro.wav', 'cinco.wav', 'seis.wav', 'siete.wav','ocho.wav', 'nueve.wav']
    odir = '/home/peima/FTP/test/audio/numbers/'
    for digit in digits:
        dir = odir + dirs[digit]
        Play(dir)
        time.sleep(0.5)
    return

def audio_recive():
    """Plays the recive message audio"""
    dir = '/home/peima/FTP/test/audio/general/1-3.wav'
    Play(dir)
    return
    
def play_tone(number):
    dirs = ['tone0', 'tone1', 'tone2', 'tone3', 'tone4', 'tone5', 'tone6', 'tone7', 'tone8', 'tone9']
    odir = '/home/peima/FTP/test/audio/general/tone/number/'  
    dir = odir + dir[number]
    Play(dir)
    return
    
def audio_message(code: str = None):
    """Plays a message, if code not given will play random, otherwise the code, if it doesn't exist returns false

    Args:
        code (str, optional): Code to be played. Defaults to None.

    Returns:
        False: The code given doesn't exist
    """
    dir = '/home/peima/FTP/test/recordings'
    listdir = os.listdir(dir)
    if code == None:
        dir2= '/home/peima/FTP/test/audio/general/1-3.wav'
        code = random.choice(listdir)
        code = dir + '/' + code
        Play(dir2)
    else:
        code = code + '.wav'
        if not code in listdir:
            code = ''
            return False
    tone_beep()
    time.sleep(0.1)
    Play(code)
    return True

def audio_code_retry():
    dir = '/home/peima/FTP/test/audio/general/3-1.wav' 
    Play(dir) 
    return    

def audio_finish():
    """Plays the finishing audio"""
    dir = '/home/peima/FTP/test/audio/general/4.wav'
    Play(dir) 
    return


def record(max_time = 60, name: str = None):
    a = SharedMemory(name="Memory", create=False)
    j = True
    rec = Recorder()
    finish_time = time.time() + max_time
    tone_beep()
    rec.start()
    if name == None:
        name = filename()
    while j == True:
        f = a.buf[0]
        if time.time() >= finish_time:
            j = False
        elif f == 1:
            j = False
    rec.stop()
    rec.save(str(name))
    return str(name)

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
            if key.buf[0] == 9:
                j = False
                recorder_main(again = True, name = name)
            elif endtime >= time.time():
                j = False
    time.sleep(0.5)
    audio_record_finish()
    time.sleep(0.5)
    play_digits(int(name))
    time.sleep(1)
    audio_recive()
    time.sleep(0.5)
    audio_message()