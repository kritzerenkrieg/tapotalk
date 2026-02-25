for f in *.mp3 *.wav *.m4a *.aac; do
  [ -e "$f" ] || continue
  ffmpeg -y -i "$f" \
    -c:a pcm_s16le \
    -ar 8000 \
    -ac 1 \
    "${f%.*}.wav"
done