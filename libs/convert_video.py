import ffmpeg
import os

from libs.convert import Convert

class ConvertVideo(Convert):

    def __init__(self, input_path: str):

        super().__init__(input_path)
        
        try:
            input_probe = ffmpeg.probe(input_path)

        except ffmpeg.Error as e:
            print('[ERROR] ' + str(e.stderr).split("\\n")[-2])
            exit()

        self.input_video_info = next(stream for stream in input_probe['streams'] if stream['codec_type'] == 'video')
        self.input_fps = self.get_video_fps(self.input_video_info)

    def generate_palette(self, reserve_transparency='False'):

        (
            ffmpeg
            .input(self.input_path)
            .filter(filter_name='palettegen', reserve_transparent=str(reserve_transparency))
            .output(self.output_palette)
            .overwrite_output()
            .run()
        )

        self.transparency = reserve_transparency

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
        print(f"Optimisation:   Level {self.optimisation_level}")
        print(f"Compression:    {self.compression_level} allowable artefacts")
        print(f"Transparency:   {self.transparency}")