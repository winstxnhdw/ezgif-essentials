import os
import subprocess

import ffmpeg
from typing_extensions import Self


class Convert:

    def __init__(self, input_path: str, transparency: bool):
        
        output_name = input_path.split('.')[0]
        self.input_path = input_path
        self.transparency = transparency
        self.output_path = f"{output_name}_converted.gif"
        self.output_palette = f"{output_name}_palette.png"

        self.optimisation_level = 0
        self.compression_level = 0

        self.get_video_info = lambda streams: next(stream for stream in streams if stream['codec_type'] == 'video') 
        

    def generate_palette(self, stream) -> Self:

        stream = ffmpeg.filter(stream, filter_name='palettegen', reserve_transparent=str(self.transparency))
        stream = ffmpeg.output(stream, self.output_palette)
        stream = ffmpeg.overwrite_output(stream)
        ffmpeg.run(stream)

        return self

    def to_gif(self, stream) -> Self:

        stream = ffmpeg.output(stream, self.output_path)
        stream = ffmpeg.overwrite_output(stream)
        ffmpeg.run(stream)

        return self

    def get_video_fps(self, video_info: dict) -> int:

        return int(eval(video_info['avg_frame_rate']))

    def get_video_resolution(self, video_info: dict) -> str:

        return f"{video_info['width']}x{video_info['height']}"

    def get_video_duration(self, video_info: dict) -> float:

        return round(float(video_info['duration']), 2)

    def clear_temp_files(self):

        os.remove(self.output_palette)

    def optimize_gif(self, optimisation_level: int):

        subprocess.run(['gifsicle', f'-O{optimisation_level}', self.output_path, '-o', self.output_path])
        self.optimisation_level = optimisation_level

    def compress_gif(self, lossy: int):
        
        subprocess.run(['gifsicle', self.output_path, f'--lossy={max(min(lossy, 200), 0)}', '-o', self.output_path])
        self.compression_level = lossy

    def print_output_info(self) -> tuple[int, float, str, int]:

        os.system('cls' if os.name=='nt' else 'clear')

        output_probe = ffmpeg.probe(self.output_path)
        output_video_info = self.get_video_info(output_probe['streams'])

        output_fps = self.get_video_fps(output_video_info)
        output_duration = self.get_video_duration(output_video_info)
        output_resolution = self.get_video_resolution(output_video_info)
        output_frames = output_video_info['nb_frames']

        title = "VIDEO HAS BEEN SUCCESSFULLY CONVERTED"
        print(title)
        print("="*len(title))
        
        return output_fps, output_duration, output_resolution, output_frames
