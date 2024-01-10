import pyaudio
import wave
from cogs.ignore import noalsaerr, nojackerr

def Player(file_name):
    # Make sure the user is reading a wav file
    if (file_name[-4:] != ".wav"):
        wf = wave.open(file_name + ".wav", "rb")
    else:
        wf = wave.open(file_name, "rb")
    try:
        with noalsaerr():
            pa = pyaudio.PyAudio()
    except:
        pa = pyaudio.PyAudio()
    device_info = pa.get_default_host_api_info()
    stream_out = pa.open(
        format = pa.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = wf.getframerate(),
        output = True,
        # output_device_index = 1,
        frames_per_buffer = 1024
    )
    data = wf.readframes(1024)
    # Will loop until there is no more remaining audio
    print("Playing Audio...")
    while len(data) > 0:
        # Play the audio file
        stream_out.write(data)
        data = wf.readframes(1024)
    stream_out.stop_stream()
    stream_out.close()
    pa.terminate()
	
if __name__ == "__main__":
	Player(input("Enter the name of the audio file: "))