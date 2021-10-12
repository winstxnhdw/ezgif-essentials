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

        (
            ffmpeg
            .input(self.input_path, pattern_type='glob')
            .filter(filter_name='palettegen', reserve_transparent=str(reserve_transparency))
            .output(self.output_palette)
            .overwrite_output()
            .run()
        )

        self.transparency = reserve_transparency

    def to_gif(self):
        
        (
            ffmpeg.filter([
                ffmpeg.input(self.input_path, pattern_type='glob', framerate=self.sequence_fps),
                ffmpeg.input(self.output_palette)],
                filter_name='paletteuse',
                dither='none'
            )
            .output(self.output_path)
            .overwrite_output()
            .run()
        )

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
        print(f"Name:           {self.output_path}")
        print(f"FPS:            {output_fps}")
        print(f"Duration:       {output_duration}s")
        print(f"Resolution:     {output_resolution}")
        print(f"Frames:         {output_frames}")
        print(f"Optimisation:   Level {self.optimisation_level}")
        print(f"Compression:    {self.compression_level} allowable artefacts")
        print(f"Transparency:   {self.transparency}")