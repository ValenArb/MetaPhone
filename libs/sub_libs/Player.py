import pyaudio
import wave
from queue import Queue  # Import for thread-safe queue
import threading  # Import for threading
from variables import *  # Assuming this holds variables like Audio_Multiplier

def Player(file_name, type=1, coder=None):
    if type == 1 or coder <= 19:
        Volume_Multiplier = Audio_Multiplier
    else:
        Volume_Multiplier = Recording_Multiplier

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

    stream_out = pa.open(
        format=pa.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
        output_device_index=1,
        frames_per_buffer=512
    )

    # Create a thread-safe queue for audio data chunks
    audio_queue = Queue()

    def play_audio_stream(stream):
        while True:
            data_chunk = audio_queue.get()
            if data_chunk is None:
                break
            stream.write(data_chunk)
        stream.stop_stream()
        stream.close()
        audio_queue.task_done()  # Signal task completion for cleanup

    def read_and_queue_audio(filename):
        with wave.open(filename, 'rb') as wav_file:
            data = wav_file.readframes(512)

            while data:
                audio_queue.put(data)  # Add data chunk to queue
                data = wav_file.readframes(512)

        audio_queue.put(None)  # Signal end of audio data for cleanup

    # Read and queue audio data in a separate thread
    read_thread = threading.Thread(target=read_and_queue_audio, args=(file_name,))
    read_thread.start()

    # Play audio from the queue in a separate thread
    play_thread = threading.Thread(target=play_audio_stream, args=(stream_out,))
    play_thread.start()

    # Wait for playback to finish (optional)
    audio_queue.join()  # Wait for all queued tasks to complete (threads finish)
    pa.terminate()  # Close PyAudio instance after playback

if __name__ == "__main__":
    Player(input("Enter the name of the audio file: "))
