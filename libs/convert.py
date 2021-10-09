import subprocess

class Convert:

    def __init__(self, input_path: str):

        self.input_path = input_path
        self.output_path = f"{self.input_path.split('.')[0]}_converted.gif"

    def optimize_gif(self):

        subprocess.run(['gifsicle', '-O3', self.output_path, '-o', self.output_path])