from libs.sub_libs.Player import Player as Play

def play_welcome():
    dir = '/home/peima/FTP/test/Audios/welcome.wav'
    Play(dir)

def play_record():
    dir = '/home/peima/FTP/test/Audios/Record.wav'
    Play(dir)
    
def play_finish():
    dir = '/home/peima/FTP/test/Audios/Finish.wav'
    Play(dir)

def play_code():
    dir = '/home/peima/FTP/test/Audios/Code.wav'
    Play(dir)
    
def play_record_finish():
    dir = '/home/peima/FTP/test/Audios/RecordEnd.wav'
    Play(dir)
    
def play_digits(digit):
    dirs = ['cero.wav', 'uno.wav', 'dos.wav', 'tres.wav', 'cuatro.wav', 'cinco.wav', 'seis.wav', 'siete.wav','ocho.wav', 'nueve.wav']
    odir = '/home/peima/FTP/test/Audios/'   
    # odir = 'C:/Users/Peima VM/Desktop/Metaphone/Audios/'
    dir = odir + dirs[digit]
    Play(dir)

def play_message_code():
    dir = '/home/peima/FTP/test/Audios/Message_code.wav'
    Play(dir)