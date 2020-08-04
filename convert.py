import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
import sys

# installation
# install Python 3.7
# install Homebrew
# - /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
# use Homebrew to install ffmpeg
# - brew install ffmpeg
# pip install python-ffmpeg-video-streaming
# python convert.py


def monitor(ffmpeg, duration, time_, process):
    per = round(time_ / duration * 100)
    sys.stdout.write("\rTranscoding...(%s%%) [%s%s]" % (per, '#' * per, '-' * (100 - per)))
    sys.stdout.flush()


with open('movies.txt') as file:
    lines = [line.rstrip('\n') for line in file]

print(f'converting {lines}')

for filename in lines:
    try:
        video = ffmpeg_streaming.input(f'./{filename}')

        # uncomment the resolutions you want
        # _144p  = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
        # _240p  = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
        # _360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
        # _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
        # _720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
        _1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))
        # _2k    = Representation(Size(2560, 1440), Bitrate(6144 * 1024, 320 * 1024))
        # _4k    = Representation(Size(3840, 2160), Bitrate(17408 * 1024, 320 * 1024))

        hls = video.hls(Formats.h264())
        hls.representations(_1080p)
        folder_name = filename.split('.')[0]
        hls.output(f'./{folder_name}/{filename}.m3u8', monitor=monitor)
    except Exception:
        print(f'could not convert {filename}')

