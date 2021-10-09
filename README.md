# ezgif-essentials
**Want to generate GIFs of the highest quality? Tired of having too many unecessary parameters? You also happen to be a motion graphic designer?** `ezgif-essentials` is a pseudo-opinionated video/sequence to GIF CLI converter. It uses the same robust conversion pipeline as [ezGIF](https://ezgif.com/) without the frame rate limitations or involuntary compression. It is powered by [FFmpeg](https://github.com/kkroening/ffmpeg-python) and [Gifsicle](https://github.com/kohler/gifsicle)

> WARNING: Image sequence conversions are garbage at the moment

## Installation
```bash
$ git clone https://github.com/winstxnhdw/ezgif-essentials.git
$ pip install -r requirements.txt
$ sudo apt install gifsicle
$ python main.py -h
```

## Usage (Video)
```bash
$ python main.py -i test.mp4 -z 3
```

```yaml
Optional arguments:
-h, --help              show this help message and exit
-z, --optimise          optimise GIF file size with zero quality penalty
-l, --lossy             applies compression by allowing some artefacts
-w, --no-transparent    disable transparency
```

## Usage (Sequence)
```bash
$ python main.py -i 'image/*.png' -a -r 50
```

```yaml
Optional arguments:
-h, --help              show this help message and exit
-a, --assemble          prepares the script for an image sequence
-r, --fps               set the fps of the resultant GIF
```
> WARNING: Make sure your file path is quoted, as asterisks are part of the shell's syntax