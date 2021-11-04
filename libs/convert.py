import os
import subprocess
import ffmpeg

class Convert:

    def __init__(self, input_path: str):

        self.input_path = input_path
        self.output_path = f"{self.input_path.split('.')[0]}_converted.gif"
        self.output_palette = f"{self.output_path.split('.')[0]}_palette.png"

        self.transparency = None
        self.optimisation_level = 0
        self.compression_level = 0

    def generate_palette(self, stream, reserve_transparency):

        stream = ffmpeg.filter(stream, filter_name='palettegen', reserve_transparent=str(reserve_transparency))
        stream = ffmpeg.output(stream, self.output_palette)
        stream = ffmpeg.overwrite_output(stream)
        ffmpeg.run(stream)

        self.transparency = reserve_transparency

    def to_gif(self, stream):

        stream = ffmpeg.output(stream, self.output_path)
        stream = ffmpeg.overwrite_output(stream)
        ffmpeg.run(stream)

    def get_video_fps(self, video_info):

        avg_frame_rate = video_info['avg_frame_rate'].split('/')
        return int(float(avg_frame_rate[0])/float(avg_frame_rate[1]))

    def get_video_resolution(self, video_info):

        return f"{video_info['width']}x{video_info['height']}"

    def get_video_duration(self, video_info):

        return round(float(video_info['duration']), 2)

    def clear_temp_files(self):

        os.remove(self.output_palette)

    def optimize_gif(self, optimisation_level):

        subprocess.run(['gifsicle', f'-O{optimisation_level}', self.output_path, '-o', self.output_path])
        self.optimisation_level = optimisation_level

    def compress_gif(self, lossy):

        subprocess.run(['gifsicle', self.output_path, f'--lossy={lossy}', '-o', self.output_path])
        self.compression_level = lossy

    def print_output_info(self):

        os.system('cls' if os.name=='nt' else 'clear')

        output_probe = ffmpeg.probe(self.output_path)
        output_video_info = next(stream for stream in output_probe['streams'] if stream['codec_type'] == 'video')

        output_fps = self.get_video_fps(output_video_info)
        output_duration = self.get_video_duration(output_video_info)
        output_resolution = self.get_video_resolution(output_video_info)
        output_frames = output_video_info['nb_frames']

        title = "VIDEO HAS BEEN SUCCESSFULLY CONVERTED"
        print(title)
        print("="*len(title))
        
        return output_fps, output_duration, output_resolution, output_frames
