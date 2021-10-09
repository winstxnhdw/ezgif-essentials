import ffmpeg

from libs.convert import Convert

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