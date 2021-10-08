import ffmpeg
import argparse
import subprocess
import os
import math as m

class Convert:

    def __init__(self, input_path: str):

        self.input_path = input_path
        self.output_path = f"{self.input_path.split('.')[0]}_converted.gif"

    def optimize_gif(self):

        subprocess.run(['gifsicle', '-O3', self.output_path, '-o', self.output_path])

class ConvertSequence(Convert):

    def __init__(self, input_path: str, sequence_fps: int):

        super().__init__(input_path)

        self.sequence_fps = sequence_fps
        self.output_path = 'sequence_converted.gif'

    def to_gif(self):

        (
            ffmpeg
            .input(self.input_path, pattern_type='glob', framerate=self.sequence_fps)
            .output(self.output_path)
            .overwrite_output()
            .run()
        )

class ConvertVideo(Convert):

    def __init__(self, input_path: str):

        super().__init__(input_path)
        
        try:
            input_probe = ffmpeg.probe(input_path)

        except ffmpeg.Error as e:
            print('[ERROR] ' + str(e.stderr).split("\\n")[-2])
            exit()

        self.output_palette = f"{self.output_path.split('.')[0]}_palette.png"
        self.input_video_info = next(stream for stream in input_probe['streams'] if stream['codec_type'] == 'video')
        self.input_fps = self.get_video_fps(self.input_video_info)

    def get_video_fps(self, video_info):

        avg_frame_rate = video_info['avg_frame_rate'].split('/')
        return int(m.floor(float(avg_frame_rate[0])/float(avg_frame_rate[1])))

    def get_video_resolution(self, video_info):

        return f"{video_info['width']}x{video_info['height']}"

    def get_video_duration(self, video_info):

        return round(float(video_info['duration']), 2)

    def generate_palette(self, reserve_transparent='True'):

        (
            ffmpeg
            .input(self.input_path)
            .filter(filter_name='palettegen', reserve_transparent=reserve_transparent)
            .output(self.output_palette)
            .overwrite_output()
            .run()
        )

    def to_gif(self):

        (
            ffmpeg.filter([
                ffmpeg.input(self.input_path, r=self.input_fps if self.input_fps <= 50 else 50),
                ffmpeg.input(self.output_palette)],
                filter_name='paletteuse',
                dither='none'
            )
            .output(self.output_path)
            .overwrite_output()
            .run()
        )

    def clear_temp_files(self):

        os.remove(self.output_palette)

    def print_output_info(self):

        os.system('cls' if os.name=='nt' else 'clear')

        output_probe = ffmpeg.probe(self.output_path)
        output_video_info = next(stream for stream in output_probe['streams'] if stream['codec_type'] == 'video')

        output_fps = self.get_video_fps(output_video_info)
        output_duration = self.get_video_duration(output_video_info)
        output_resolution = self.get_video_resolution(output_video_info)
        output_frames = output_video_info['nb_frames']

        input_duration = self.get_video_duration(self.input_video_info)
        input_resolution = self.get_video_resolution(self.input_video_info)
        input_frames = self.input_video_info['nb_frames']

        title = "VIDEO HAS BEEN SUCCESSFULLY CONVERTED"
        print(title)
        print("="*len(title))
        print(f"Name:           {self.output_path} <- {self.input_path}")
        print(f"FPS:            {output_fps} <- {self.input_fps}")
        print(f"Duration:       {output_duration}s <- {input_duration}s")
        print(f"Resolution:     {output_resolution} <- {input_resolution}")
        print(f"Frames:         {output_frames} <- {input_frames}")

def main(args):

    if args.convert_type == 'vid':
        convert_video = ConvertVideo(args.input)
        convert_video.generate_palette(args.no_transparent)
        convert_video.to_gif()
        convert_video.clear_temp_files()
        convert_video.print_output_info()

    elif args.convert_type == 'seq':
        convert_sequence = ConvertSequence(args.input, args.fps)
        convert_sequence.to_gif()

def parse_args():

    parser = argparse.ArgumentParser(description='Converts video/sequence to GIF')
    parser.add_argument('-i', '--input', type=str, metavar='', help='Input file path', required=True)

    subparser = parser.add_subparsers(dest='convert_type')

    video_parser = subparser.add_parser('vid', help="Converts video to GIF")
    video_parser.add_argument('-w', '--no-transparent', action='store_false', help='Disable transparency', required=False)
    video_parser.add_argument('-l', '--lossy', type=int, default=None, metavar='', help='No. of artifacts allowed', required=False)
    video_parser.add_argument('-z', '--optimise', type=int, default=None, metavar='', help='Optimise GIF file size (1 - 3)', required=False)
    
    sequence_parser = subparser.add_parser('seq', help="Converts sequence to GIF")
    sequence_parser.add_argument('-r', '--fps', type=int, default=50, metavar='', help='Sequence FPS', required=False)

    return parser.parse_known_args()

if __name__ == '__main__':
    args, _ = parse_args()
    main(args)