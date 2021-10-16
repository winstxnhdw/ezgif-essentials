import subprocess
import os
import math as m

class Convert:

    def __init__(self, input_path: str):

        self.input_path = input_path
        self.output_path = f"{self.input_path.split('.')[0]}_converted.gif"
        self.output_palette = f"{self.output_path.split('.')[0]}_palette.png"

        self.transparency = None
        self.optimisation_level = 0
        self.compression_level = 0

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
