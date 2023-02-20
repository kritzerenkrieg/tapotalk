import sys
import threading
import time
import multiprocessing
from multiprocessing import Queue
import asyncio

from TapoTalk import TapoTalk

# ffmpeg -y -i ~/aligator.wav -acodec pcm_s16le -f s16le -ac 1 -ar 8000 -blocksize 1504 pipe: | python3 trubka.py

IP = "192.168.0.123"
USER = "greta"
CLOUD_PASSWORD = "1234"
SUPER_SECRET = "dadada"

talk = TapoTalk(IP, USER, CLOUD_PASSWORD, SUPER_SECRET, encrypt=True)
asyncio.run(talk.half_duplex_start())

queue = Queue()
data = []
posilat = True


def send_chunk(chunk_data):
    asyncio.run(talk.process_and_send_audio_chunk(chunk_data))


def process_buffer():
    while True:
        try:
            if not queue.empty():
                chunk = queue.get()
                send_chunk(chunk)

            time.sleep(TapoTalk.CHUNK_LEN / 8000 / 2)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":

    thread = multiprocessing.Process(target=process_buffer)
    thread.start()

    last = time.time()
    while True:
        try:
            
            if queue.qsize() > 32:
                time.sleep(0.01)
                continue
            
            in_data = sys.stdin.buffer.read(TapoTalk.CHUNK_LEN)
            if in_data is not b"":
                last = time.time()
            else:
                if time.time() - last > 5 and queue.empty():
                    print("dlouho nic neprislo a fronta je prazdna - koncim!!!!")
                    thread.terminate()
                    break

            data += [
                int.from_bytes(in_data[i : i + 1], byteorder="big", signed=True)
                for i in range(len(in_data))
            ]

            while len(data) > TapoTalk.CHUNK_LEN:
                queue.put(data[: TapoTalk.CHUNK_LEN])
                data = data[TapoTalk.CHUNK_LEN :]
            time.sleep(0.01)
        except KeyboardInterrupt:
            break

    thread.join()
    asyncio.run(talk.half_duplex_stop())

    print("hotovo!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
