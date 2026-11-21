#!/usr/bin/env bash
# تصفية التعليق الصوتي ومزجه مع المؤثرات (بدون موسيقى) وتركيبه على الفيديو
# الاستخدام: bash clean_voice.sh IMG_7169.mov dabrah-v5-captions.mp4 out.mp4
set -e
IN="$1"; VIDEO="$2"; OUT="$3"
ffmpeg -y -loglevel error -i "$IN" -vn -ac 1 -ar 48000 raw.wav
F="highpass=f=110,highpass=f=110,lowpass=f=11000,afftdn=nr=18:nf=-46:tn=1,agate=threshold=0.018:ratio=2.5:range=0.25:attack=8:release=180,equalizer=f=300:t=q:w=1.2:g=-2,equalizer=f=3000:t=q:w=1.5:g=2.5,equalizer=f=8000:t=h:w=0.7:g=1.5,deesser=i=0.3,acompressor=threshold=0.09:ratio=2.8:attack=8:release=120:makeup=1.5"
ffmpeg -y -loglevel error -i raw.wav -af "$F" -ar 48000 stage1.wav
ffmpeg -y -loglevel error -i stage1.wav -af "loudnorm=I=-16:TP=-1.5:LRA=9" -ar 48000 voice_clean.wav
# sfx.wav يتولد من make_sfx.py (نقرات وانتقالات على توقيت الفيديو)
ffmpeg -y -loglevel error -i voice_clean.wav -i sfx.wav -filter_complex "[0:a]atrim=start=0.45,asetpts=PTS-STARTPTS,apad=whole_dur=80,atrim=0:80,afade=t=out:st=79.5:d=0.5,pan=stereo|c0=c0|c1=c0[v];[1:a]atrim=0:80[s];[v][s]amix=inputs=2:normalize=0,alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5:LRA=11[m]" -map "[m]" -ar 48000 mix.wav
ffmpeg -y -loglevel error -i "$VIDEO" -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
echo "done → $OUT"
