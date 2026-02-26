import asyncio
import os
import sys
import signal
import argparse

from .tapo_core import TapoTalk


class MicrophoneStreamer:
    """Async microphone streamer that pushes audio to `TapoTalk`.

    This wrapper keeps the existing `TapoTalk` logic and provides an
    asyncio-friendly producer/consumer using `pyaudio` and `asyncio.Queue`.
    """

    def __init__(self, host, user, cloud_password, super_secret_key, encrypt=False, rate=8000):
        self.talk = TapoTalk(host, user, cloud_password, super_secret_key, encrypt=encrypt)
        self.rate = rate
        self._queue = asyncio.Queue()
        self._pyaudio = None
        self._stream = None
        self._consumer_task = None

    async def start(self):
        await self.talk.half_duplex_start()

        import pyaudio

        self._pyaudio = pyaudio.PyAudio()

        loop = asyncio.get_event_loop()

        def callback(in_data, frame_count, time_info, status):
            # Push raw bytes to asyncio queue from the audio thread
            loop.call_soon_threadsafe(self._queue.put_nowait, in_data)
            return (None, pyaudio.paContinue)

        self._stream = self._pyaudio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            stream_callback=callback,
        )
        self._stream.start_stream()

        self._consumer_task = asyncio.create_task(self._consumer())

    async def _consumer(self):
        while True:
            data = await self._queue.get()
            if data is None:
                break
            # Convert 16-bit little-endian samples -> signed 8-bit range (-128..127)
            samples = [
                int.from_bytes(data[i : i + 2], byteorder="little", signed=True)
                for i in range(0, len(data), 2)
            ]
            bytes8 = [max(-128, min(127, s >> 8)) for s in samples]
            try:
                await self.talk.process_and_send_audio_chunk(bytes8)
            except Exception:
                # keep consumer alive on transient errors
                continue

    async def stop(self):
        # signal consumer to finish
        await self._queue.put(None)
        if self._consumer_task:
            await self._consumer_task

        if self._stream:
            try:
                self._stream.stop_stream()
                self._stream.close()
            except Exception:
                pass

        if self._pyaudio:
            try:
                self._pyaudio.terminate()
            except Exception:
                pass

        await self.talk.half_duplex_stop()


async def _run_cli(args):
    streamer = MicrophoneStreamer(
        args.host, args.user, args.cloud_password, args.super_secret, encrypt=not args.no_encrypt, rate=args.rate
    )
    await streamer.start()

    loop = asyncio.get_event_loop()
    stop_future = loop.create_future()

    def _on_signal():
        if not stop_future.done():
            stop_future.set_result(True)

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _on_signal)
        except NotImplementedError:
            # event loop on Windows may not support signal handlers
            pass

    print("Streaming from microphone — press Ctrl-C to stop")
    await stop_future
    await streamer.stop()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Tapotalk microphone streamer")
    parser.add_argument("--host", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--cloud-password", required=True, dest="cloud_password")
    parser.add_argument("--super-secret", required=True, dest="super_secret")
    parser.add_argument("--no-encrypt", action="store_true", dest="no_encrypt", help="Disable encryption when sending audio")
    parser.add_argument("--rate", type=int, default=8000)
    args = parser.parse_args(argv)
    asyncio.run(_run_cli(args))


if __name__ == "__main__":
    main()
