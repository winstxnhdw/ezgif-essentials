import ffmpeg
import os

from libs.convert import Convert

class ConvertVideo(Convert):

    def __init__(self, input_path: str):

        super().__init__(input_path)
        
        try:
            input_probe = ffmpeg.probe(input_path)

        except ffmpeg.Error as e:
            print(f"[ERROR] {str(e.stderr).split('\\n')[-2]}")
            exit()

        self.input_video_info = next(stream for stream in input_probe['streams'] if stream['codec_type'] == 'video')
        self.input_fps = self.get_video_fps(self.input_video_info)

    def generate_palette(self, reserve_transparency='False'):

        stream = ffmpeg.input(self.input_path)
        super().generate_palette(stream, reserve_transparency)

    def to_gif(self):

        stream = ffmpeg.filter([
                 ffmpeg.input(self.input_path, r=self.input_fps if self.input_fps <= 50 else 50),
                 ffmpeg.input(self.output_palette)],
                 filter_name='paletteuse',
                 dither='none'
            )

        super().to_gif(stream)

    def print_output_info(self):

        output_fps, output_duration, output_resolution, output_frames = super().print_output_info()

        input_duration = self.get_video_duration(self.input_video_info)
        input_resolution = self.get_video_resolution(self.input_video_info)
        input_frames = self.input_video_info['nb_frames']

        print(f"Name:           {self.output_path} <- {self.input_path}")
        print(f"FPS:            {output_fps} <- {self.input_fps}")
        print(f"Duration:       {output_duration}s <- {input_duration}s")
        print(f"Resolution:     {output_resolution} <- {input_resolution}")
        print(f"Frames:         {output_frames} <- {input_frames}")
        print(f"Optimisation:   Level {self.optimisation_level}")
        print(f"Compression:    {self.compression_level} allowable artefacts")
        print(f"Transparency:   {self.transparency}")