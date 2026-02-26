from pytapo import Tapo
import time
import math
import asyncio

from .HttpAudioSession import HttpAudioSession

from .ResamplovadloFix import Resamplovadlo
from .hfix import Paketovadlo


class TapoTalk:

    CHUNK_LEN = 320 * 6  # == 1920
    TAPO_AUDIO_PCKT_LEN = 1504

    def __init__(self, host, user, cloud_password, super_secret_key, encrypt=True):
        self._paketovadlo = Paketovadlo()

        self._tapo_ses = HttpAudioSession(
            ip=host, cloud_password=cloud_password, username=user, super_secret_key=super_secret_key
        )
        self._ses_id = -1
        self._timestamp = 0
        self._encrypt = encrypt

    async def half_duplex_start(self) -> None:

        if not self._tapo_ses._started:
            await self._tapo_ses.start()

        rt = self._tapo_ses.transceive_keepSession(
            data='{"type": "request","seq":1, "params": {"talk": {"mode": "half_duplex"}, "method": "get"}}',
            mimetype="application/json",
            encrypt=True,
        )
        async for h in rt:
            self._ses_id = h.session

    async def half_duplex_stop(self) -> None:
        rt = self._tapo_ses.transceive_keepSession(
            data='{"type":"request","seq":2,"params":{"stop":"null","method":"do"}}',
            mimetype="application/json",
            encrypt=True,
            session=self._ses_id,
        )
        async for h in rt:
            pass

    def process_audio_file(self, wav_filename) -> bytearray:
        wav = open(wav_filename, "rb")
        data = wav.read()

        data = [
            int.from_bytes(data[44 + i : 45 + i], byteorder="big", signed=True)
            for i in range(len(data) - 44)
        ]

        stream = []

        chunku = math.ceil(len(data) / TapoTalk.CHUNK_LEN)
        self._timestamp = round(time.time() * 1000)

        for i in range(chunku):
            chunk = data[i * TapoTalk.CHUNK_LEN : (i + 1) * (TapoTalk.CHUNK_LEN) + 0]
            chunk = Resamplovadlo.b(chunk, len(chunk))
            _len = len(chunk)
            chunk = self._paketovadlo.k(chunk, _len, self._timestamp)
            stream += chunk
            self._timestamp += round(_len * 90000 / 8000)

        stream = [x if x > -1 else (256 + x) for x in stream]
        return bytearray(stream)

    async def _play_ts_file(self, ts_filename) -> None:

        await self.half_duplex_start()

        in_file = open(ts_filename, "rb")
        data = in_file.read()
        in_file.close()

        packetu = math.ceil(len(data) / TapoTalk.TAPO_AUDIO_PCKT_LEN)
        for i in range(packetu):
            packet = data[
                i * TapoTalk.TAPO_AUDIO_PCKT_LEN : (i + 1) * TapoTalk.TAPO_AUDIO_PCKT_LEN
            ]
            time.sleep((TapoTalk.CHUNK_LEN) / (8000) / 2)
            await self._tapo_ses.transceive_audio(
                data=packet, encrypt=self._encrypt, session=self._ses_id
            )

        await self.half_duplex_stop()

    async def send_pcma_packet(self, data):
        rt = await self._tapo_ses.transceive_audio(
            data=data, encrypt=self._encrypt, session=self._ses_id
        )

    def process_audio_chunk(self, chunk):
        chunku = math.ceil(len(chunk) / TapoTalk.CHUNK_LEN)
        if self._timestamp == 0:
            self._timestamp = round(time.time() * 1000)
        chunk = Resamplovadlo.b(chunk, len(chunk))
        _len = len(chunk)
        chunk = self._paketovadlo.k(chunk, _len, self._timestamp)
        self._timestamp += round(_len * 90000 / 8000)
        chunk = [x if x > -1 else (256 + x) for x in chunk]
        return bytearray(chunk)

    async def process_and_send_audio_chunk(self, data):
        data = self.process_audio_chunk(data)
        await self.send_pcma_packet(data)

    def wav2ts(self, wav_filename, out_filename):
        stream = self.process_audio_file(wav_filename)
        out = open(out_filename, "wb")
        out.write(stream)
        out.close()

    async def stream_wav(self, wav_filename) -> None:
        await self.half_duplex_start()
        if not self._tapo_ses._started:
            await self._tapo_ses.start()
        wav = open(wav_filename, "rb")
        data = wav.read()
        data = [
            int.from_bytes(data[44 + i : 45 + i], byteorder="big", signed=True)
            for i in range(len(data) - 44)
        ]

        chunku = math.ceil(len(data) / TapoTalk.CHUNK_LEN)
        self._timestamp = round(time.time() * 1000)

        stream = []

        for i in range(chunku):
            chunk = data[i * TapoTalk.CHUNK_LEN : (i + 1) * TapoTalk.CHUNK_LEN]
            chunk = Resamplovadlo.b(chunk, len(chunk))
            _len = len(chunk)
            chunk = self._paketovadlo.k(chunk, _len, self._timestamp)
            chunk = [x if x > -1 else (256 + x) for x in chunk]
            stream += chunk
            self._timestamp += round(_len * 90000 / 8000)
            if len(stream) >= 1504:
                chunk = bytes(stream[:1504])
                stream = stream[1504:]
                rt = await self._tapo_ses.transceive_audio(
                    data=chunk, encrypt=self._encrypt, session=self._ses_id
                )
                time.sleep((TapoTalk.CHUNK_LEN) / (8000) / 2)

        await self.half_duplex_stop()

    def ts2camera(self, ts_filename) -> None:
        asyncio.run(self._play_ts_file(ts_filename))

    def streamovat(self, filename) -> None:
        asyncio.run(self.stream_wav(filename))
