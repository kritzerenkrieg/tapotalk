from pytapo import Tapo
import time
import math
import asyncio

from HttpAudioSession import HttpAudioSession

from ResamplovadloFix import Resamplovadlo
from hfix import Paketovadlo

class TapoTalk:

    # dýlka audiochunků
    # min. možná dýlka podle java zdrojačku je 320 zorků
    # předpokládám že idelál bude ňákej malej násobek čisla 80,160, nebo pravě 320

    # hodnota by měla bejt v rosahu 1810 - 2177 (včetně) protože
    # v tomdlectom intervalu nám Packetovadlo generuje právě 8 chunků
    # který daj dohormady přesně těch 1504 bytů stejně jako v tamtom
    # jejich origo audiopacketu
    CHUNK_LEN = 320 * 6  # == 1920
    # CHUNK_LEN = 1810 # minimální možnej počet zorků pro vyrobení osmi paketů
    # CHUNK_LEN = 2177 # maximální možnej počet zorků pro vyrobení osmi paketů

    # dylka puvodního audiopacketu
    TAPO_AUDIO_PCKT_LEN = 1504

    def __init__(self, host, user, cloud_password, super_secret_key, encrypt=True):
        self._paketovadlo = Paketovadlo()

        # upravená HttpMediaSession z knihovy Tapo
        self._tapo_ses = HttpAudioSession(
            ip=host, cloud_password=cloud_password, username=user, super_secret_key=super_secret_key
        )
        self._ses_id = -1
        self._timestamp = 0
        self._encrypt = encrypt

    # request kterej to dělá nazačátku zapnutí mluvení do kamery
    async def half_duplex_start(self) -> None:

        if not self._tapo_ses._started:
            await self._tapo_ses.start()

        # pole 'seq' nám přepiše tapo knihovna
        rt = self._tapo_ses.transceive_keepSession(
            data='{"type": "request","seq":1, "params": {"talk": {"mode": "half_duplex"}, "method": "get"}}',
            mimetype="application/json",
            encrypt=True,
        )
        async for h in rt:
            self._ses_id = h.session

    # .......a navopak request kterej to dělá při skončení mluvení
    async def half_duplex_stop(self) -> None:
        # pole 'seq' nám zase přepiše knihovna
        rt = self._tapo_ses.transceive_keepSession(
            data='{"type":"request","seq":2,"params":{"stop":"null","method":"do"}}',
            mimetype="application/json",
            encrypt=True,
            session=self._ses_id,
        )
        async for h in rt:
            pass

    # překodování *.wav souboru do *.mp2t/*.ts formátu kterýmu rozumí Tapokamerka
    # pomocí pučenýho zdrojáku z offiko android appky
    # wav by měl bejt:
    # monochannel PCMA encoded *.wav file, sample rate 8KHz, 16bit precision
    def process_audio_file(self, wav_filename) -> bytearray:
        wav = open(wav_filename, "rb")
        data = wav.read()
        print(data)

        # ucvaknem hlavičku wav souboru a načtem jenom zvukový data
        # (hlavička *.wav souboru je prej dycky 44 bytů dlouhá)
        # a převedem do javovskýho rosahu
        # funkce který jsme si vypučili z android appky vočekávaj hodnoty
        # bytů jako v javě, java dělá s bytama jinak než python, v pythonu
        # je byte v rosahu 0 až 255, v javě -128 až 127
        data = [
            int.from_bytes(data[44 + i : 45 + i], byteorder="big", signed=True)
            for i in range(len(data) - 44)
        ]

        stream = []

        chunku = math.ceil(len(data) / TapoTalk.CHUNK_LEN)
        self._timestamp = round(time.time() * 1000)

        for i in range(chunku):
            chunk = data[i * TapoTalk.CHUNK_LEN : (i + 1) * (TapoTalk.CHUNK_LEN) + 0]

            # imo trošku lepčejšího zvuku s míň klapání de dosahnout jednoduše malým overlapem
            # sousednich packetů ale možná se mi to jenom zdá jak si to furt pouštim dokolečka :O :O
            # chunk = data[ i * TapoTalk.CHUNK_LEN : (i+1) * (TapoTalk.CHUNK_LEN) + 80]
            chunk = Resamplovadlo.b(chunk, len(chunk))

            # převedeme audiostream na mp2t pakety prostrčením tou javovskou třídou
            _len = len(chunk)
            chunk = self._paketovadlo.k(chunk, _len, self._timestamp)
            stream += chunk

            # zvedneme hodnotu _timestampu uplně stejně jako javovskej kód
            # skutečnej čas si to bere jenom nazačátku a ani tam možná neni skutečnej nutnej :O ;D
            # duležitej je už jenom relativní čas jednotlivejch paketů mp2t streamu
            self._timestamp += round(_len * 90000 / 8000)

        # převedeme z rosahu hodnot javovovejch bytů (-128 až 127) do rosahu
        # hodnot pythoních bytů (0 až 255)
        stream = [x if x > -1 else (256 + x) for x in stream]
        return bytearray(stream)

    # přehraje zakodovanej mp2t audiostream ze souboru
    # asi by to měl bejt *.ts soubor vyrobenej timdlectim algoritmusem
    # s *.ts souborama vyrobenejma třeba ffmpegem si to vubec nerozumělo
    async def _play_ts_file(self, ts_filename) -> None:

        await self.half_duplex_start()

        in_file = open(ts_filename, "rb")
        data = in_file.read()
        in_file.close()

        # packety posíláme po vosmy najednou stejně jako voni
        # když se to nedodrží tak se kamerka muže šprajcnout a uplně se zamkne pro
        # tcp komunikaci a musí se restartovat vyndáním šňůry zezdi (reset appkou neni možnej)
        packetu = math.ceil(len(data) / TapoTalk.TAPO_AUDIO_PCKT_LEN)
        for i in range(packetu):
            packet = data[
                i
                * TapoTalk.TAPO_AUDIO_PCKT_LEN : (i + 1)
                * TapoTalk.TAPO_AUDIO_PCKT_LEN
            ]
            time.sleep(
                (TapoTalk.CHUNK_LEN) / (8000) / 2
            )  # todlecto by mělo fungovat bez dělení dvojkou ne :O :O
            await self._tapo_ses.transceive_audio(
                data=packet, encrypt=self._encrypt, session=self._ses_id
            )

        await self.half_duplex_stop()

    # wrap na poslání jendoho audio packetu
    async def send_pcma_packet(self, data):
        rt = await self._tapo_ses.transceive_audio(
            data=data, encrypt=self._encrypt, session=self._ses_id
        )

    # to samý jako process_audio_file ale pro jedinejch chunk
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

    # zpracovat + poslat skovaný v jediný metodě
    async def process_and_send_audio_chunk(self, data):
        data = self.process_audio_chunk(data)
        await self.send_pcma_packet(data)

    # zapsání wavu do *.ts
    def wav2ts(self, wav_filename, out_filename):
        stream = self.process_audio_file(wav_filename)
        out = open(out_filename, "wb")
        out.write(stream)
        out.close()

    # pokusná funkce na živý streamování ze souboru
    # jakože jestli to bude dost rychle současně číst ze souboru, převádět na mp2t a posilat do kamery
    # nóóóóóóóóóó jakštakš to de :D víc praktičtější použití je s multithreadingem
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

    # sync volání
    def ts2camera(self, ts_filename) -> None:
        asyncio.run(self._play_ts_file(ts_filename))

    def streamovat(self, filename) -> None:
        asyncio.run(self.stream_wav(filename))


if __name__ == "__main__":

    IP = "192.168.1.108"
    USER = "admin"
    CLOUD_PASSWORD = "forInovasi123"
    SUPER_SECRET = "dadada"
    
    talk = TapoTalk(IP, USER, CLOUD_PASSWORD, SUPER_SECRET, encrypt=True)

    talk.wav2ts("convert_audio/minum.wav", "fiala.ts")
    talk.ts2camera("fiala.ts")
