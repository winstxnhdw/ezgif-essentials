import ffmpeg
from typing_extensions import Self

from libs import Convert


class ImageNotSequence(Exception):
    
    def __init__(self):

        error_message = "Input is not an image sequence. If you are on Linux, make sure that you have contained your file path with quotations. For example, 'image/*.png'"
        super().__init__(error_message)

class ConvertSequence(Convert):

    def __init__(self, input_path: str, transparency: bool, sequence_fps: int):

        super().__init__(input_path, transparency)

        if '*' not in self.input_path:
            raise ImageNotSequence
        
        output_name = 'sequence_converted'
        self.sequence_fps = sequence_fps
        self.output_path = f'{output_name}.gif'
        self.output_palette = f"{output_name}_palette.png"

    def generate_palette(self) -> Self:

        stream = ffmpeg.input(self.input_path, pattern_type='glob')
        return super().generate_palette(stream)

    def to_gif(self) -> Self:
        
        stream = (
            ffmpeg.filter([
                ffmpeg.input(self.input_path, pattern_type='glob', framerate=self.sequence_fps if self.sequence_fps <= 50 else 50),
                ffmpeg.input(self.output_palette)],
                filter_name='paletteuse',
                dither='none'
            )
        )

        return super().to_gif(stream)

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
