import subprocess

class Convert:

    def __init__(self, input_path: str):

        self.input_path = input_path
        self.output_path = f"{self.input_path.split('.')[0]}_converted.gif"

        self.optimisation_level = 0
        self.compression_level = 0

    def optimize_gif(self, optimisation_level):

        subprocess.run(['gifsicle', f'-O{optimisation_level}', self.output_path, '-o', self.output_path])
        self.optimisation_level = optimisation_level

    def compress_gif(self, lossy):

        subprocess.run(['gifsicle', self.output_path, f'--lossy={lossy}', '-o', self.output_path])
        self.compression_level = lossy