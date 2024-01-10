import os

def filename():
    files = os.listdir('/home/peima/FTP/test/recordings')
    wav_files = []
    for f in files:
        if f.endswith('.wav'):
            filen = f.split('.')
            wav_files.append(int(filen[0]))
    wav_files.sort()
    for i in range(len(wav_files)):
        if wav_files[i] != i+1:
            return str(i+1)
    return str(len(wav_files)+1)