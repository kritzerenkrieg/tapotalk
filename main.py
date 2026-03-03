#!/usr/bin/env python3
"""
tapotalk_parsed.py

Utilities extracted from TapoTalk for programmatic use.

Provided functions:
- `convert_wav_to_ts(wav_path) -> bytes` : converts a PCMA 8kHz WAV into the Tapokamera .ts byte stream.
- `save_ts(ts_bytes, out_path)` : write bytes to disk.
- `send_ts_to_camera(ts_bytes, ip, user, password, secret)` : attempts to import `TapoTalk` and call `ts2camera()`; requires repo dependencies (`pytapo`, `kasa`), otherwise raises ImportError with guidance.

This module avoids importing `pytapo` while performing conversion, so it can be used in other scripts without installing networking dependencies.
"""
from __future__ import annotations

import math
import time
import tempfile
import os
from typing import Optional


def convert_wav_to_ts(wav_path: str) -> bytes:
    """Convert a WAV file (PCM A / PCMA mono 8kHz expected) into the camera .ts stream bytes.

    This implementation mirrors the logic in `TapoTalk.process_audio_file` but does not
    import `pytapo` or any network code.
    """
    # Import locally to reuse repository resampler/packet encoder
    from ResamplovadloFix import Resamplovadlo
    from hfix import Paketovadlo

    with open(wav_path, 'rb') as f:
        raw = f.read()

    if len(raw) <= 44:
        raise ValueError('wav file too small or missing data')

    payload = raw[44:]

    # Work with byte values (0..255) as in earlier repo conversion
    data_bytes = [b for b in payload]

    CHUNK_LEN = 320 * 6
    paketovadlo = Paketovadlo()
    stream = []
    chunku = math.ceil(len(data_bytes) / CHUNK_LEN)
    timestamp = round(time.time() * 1000)

    for i in range(chunku):
        chunk = data_bytes[i * CHUNK_LEN : (i + 1) * CHUNK_LEN]
        chunk = Resamplovadlo.b(chunk, len(chunk))
        _len = len(chunk)
        chunk = paketovadlo.k(chunk, _len, timestamp)
        stream += chunk
        timestamp += round(_len * 90000 / 8000)

    # Convert negative java-style bytes to python 0..255
    stream = [x if x > -1 else (256 + x) for x in stream]
    return bytes(stream)


def save_ts(ts_bytes: bytes, out_path: str) -> None:
    with open(out_path, 'wb') as f:
        f.write(ts_bytes)


def send_ts_to_camera(ts_bytes: bytes, ip: str, user: str, password: str, secret: str, cleanup: bool = True) -> None:
    """Send a .ts byte stream to camera using `TapoTalk.ts2camera`.

    This function requires `pytapo` and other network dependencies used by `TapoTalk`.
    If `TapoTalk` cannot be imported, ImportError is raised with guidance.
    """
    try:
        from TapoTalk import TapoTalk
    except Exception as exc:
        raise ImportError(
            "Unable to import TapoTalk for sending. Install repo dependencies (pytapo, kasa)."
        ) from exc

    # write temporary ts file
    fd, tmp_path = tempfile.mkstemp(suffix='.ts')
    os.close(fd)
    try:
        with open(tmp_path, 'wb') as f:
            f.write(ts_bytes)

        tt = TapoTalk(ip, user, password, secret, encrypt=True)
        tt.ts2camera(tmp_path)
    finally:
        if cleanup:
            try:
                os.remove(tmp_path)
            except OSError:
                pass


if __name__ == '__main__':
    import argparse
    import sys

    p = argparse.ArgumentParser(description='Convert WAV to Tapokamera .ts and optionally send')
    p.add_argument('ip')
    p.add_argument('user')
    p.add_argument('password')
    p.add_argument('secret')
    p.add_argument('wav')
    p.add_argument('--out-ts', help='Write converted .ts to this path (default: <wav>.ts)')
    p.add_argument('--no-send', action='store_true', help='Do not send converted .ts to camera (by default the script will attempt to send)')
    args = p.parse_args()

    try:
        ts = convert_wav_to_ts(args.wav)
    except Exception as e:
        print('Conversion failed:', e, file=sys.stderr)
        raise

    # default out-ts to wav_path + '.ts' when not provided
    out_ts_path = args.out_ts if args.out_ts else args.wav + '.ts'
    try:
        save_ts(ts, out_ts_path)
        print('Wrote', out_ts_path)
    except Exception as e:
        print('Failed to write .ts file:', e, file=sys.stderr)
        # continue; sending might still be attempted if possible

    # send by default unless --no-send was provided
    if not args.no_send:
        try:
            send_ts_to_camera(ts, args.ip, args.user, args.password, args.secret)
            print('Sent to camera')
        except ImportError as ie:
            print('Send failed - missing network deps:', ie, file=sys.stderr)
            sys.exit(2)
        except Exception as e:
            print('Send failed:', e, file=sys.stderr)
            sys.exit(3)
