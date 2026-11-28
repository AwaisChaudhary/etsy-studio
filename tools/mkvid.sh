#!/bin/bash
# Etsy listing video (about 11 s, 1350x1080, no audio): slow zoom on each listing image with crossfades.
# Usage: tools/mkvid.sh out.mp4 img1.jpg img2.jpg ... (3-5 images, 2000x1600 listing images)
set -e
OUT=$1; shift
N=$#; D=2.6; F=0.5; FPS=30
inputs=""; filt=""; i=0
for img in "$@"; do
  inputs="$inputs -i $img"
  filt="$filt[$i:v]scale=2700:2160,zoompan=z='min(zoom+0.0009,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$(python3 -c "print(int($D*$FPS))"):s=1350x1080:fps=$FPS,setsar=1,format=yuv420p[v$i];"
  i=$((i+1))
done
prev="v0"; off=$(python3 -c "print($D-$F)")
for ((k=1; k<N; k++)); do
  filt="$filt[$prev][v$k]xfade=transition=fade:duration=$F:offset=$off[x$k];"; prev="x$k"
  off=$(python3 -c "print($off+$D-$F)")
done
ffmpeg -y -loglevel error $inputs -filter_complex "${filt%;}" -map "[$prev]" -c:v libx264 -preset medium -crf 23 -movflags +faststart -an "$OUT"
echo "$OUT $(du -h "$OUT" | cut -f1)"
