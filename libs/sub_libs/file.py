import os

def filename():
    """Returns the first available number in the recordings folder"""
    files = os.listdir('/home/peima/FTP/test/recordings')
    wav_files = []
    for f in files:
        if f.endswith('.wav'):
            filen = f.split('.')
            wav_files.append(int(filen[0]))
    wav_files.sort()
    for i in range(len(wav_files)):
        if wav_files[i] != i+1:
            return i+1
    return len(wav_files)+1