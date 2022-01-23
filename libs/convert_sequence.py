import ffmpeg
import os

from libs.convert import Convert

class ConvertSequence(Convert):

    def __init__(self, input_path: str, sequence_fps: int):

        super().__init__(input_path)

        if '*' not in self.input_path:
            raise Exception("Input is not an image sequence. If you are on Linux, make sure that you have 'quoted' your file path.")

        self.sequence_fps = sequence_fps
        self.output_path = 'sequence_converted.gif'
        self.output_palette = f"{self.output_path.split('.')[0]}_palette.png"

    def generate_palette(self, reserve_transparency='False'):

        stream = ffmpeg.input(self.input_path, pattern_type='glob')
        super().generate_palette(stream, reserve_transparency)

    def to_gif(self):
        
        stream = ffmpeg.filter([
                 ffmpeg.input(self.input_path, pattern_type='glob', framerate=self.sequence_fps if self.sequence_fps <= 50 else 50),
                 ffmpeg.input(self.output_palette)],
                 filter_name='paletteuse',
                 dither='none'
        )

        super().to_gif(stream)

    def print_output_info(self):

        output_fps, output_duration, output_resolution, output_frames = super().print_output_info()

        print(f"Name:           {self.output_path}")
        print(f"FPS:            {output_fps}")
        print(f"Duration:       {output_duration}s")
        print(f"Resolution:     {output_resolution}")
        print(f"Frames:         {output_frames}")
        print(f"Optimisation:   Level {self.optimisation_level}")
        print(f"Compression:    {self.compression_level} allowable artefacts")
        print(f"Transparency:   {self.transparency}")