import pyaudio
import time
from TapoTalk import TapoTalk
import asyncio

from multiprocessing import Queue

IP = "192.168.0.123"
USER = "greta"
CLOUD_PASSWORD = "1234"
SUPER_SECRET = "dadada"

talk = TapoTalk(IP, USER, CLOUD_PASSWORD, SUPER_SECRET,encrypt=False)

asyncio.run(talk.half_duplex_start())

audio = pyaudio.PyAudio()

data = []
queue = Queue()


def send_chunk(chunk_data):
    asyncio.run(talk.process_and_send_audio_chunk(chunk_data))


def callback(in_data, frame_count, time_info, flag):

    global data
    data += [
        int.from_bytes(in_data[i : i + 1], byteorder="big", signed=True)
        for i in range(len(in_data))
    ]
    while len(data) > TapoTalk.CHUNK_LEN:

        queue.put(data[: TapoTalk.CHUNK_LEN])
        data = data[TapoTalk.CHUNK_LEN :]

    return in_data, pyaudio.paContinue


stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=8000,
    output=False,
    input=True,
    stream_callback=callback,
)

stream.start_stream()
while stream.is_active():
    try:
        if not queue.empty():
            chunk = queue.get()
            send_chunk(chunk)

        time.sleep(0.01)
    except KeyboardInterrupt:
        break

stream.stop_stream()
print("Stream is stopped")

stream.close()
audio.terminate()
asyncio.run(talk.half_duplex_stop())

print("hotovo!!!!!!!!!!!!!!!!!!!!!!!!!!!")
