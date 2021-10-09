import argparse

from libs.convert_video import ConvertVideo
from libs.convert_sequence import ConvertSequence

def main(args):

    if not args.assemble:
        convert_video = ConvertVideo(args.input)
        convert_video.generate_palette(args.no_transparent)
        convert_video.to_gif()
        convert_video.clear_temp_files()

        if args.optimise:
            convert_video.optimize_gif(args.optimise)

        if args.lossy:
            convert_video.compress_gif(args.lossy)

        convert_video.print_output_info()

    else:
        convert_sequence = ConvertSequence(args.input, args.fps)
        convert_sequence.to_gif()

        if args.optimise:
            convert_sequence.optimize_gif(args.optimise)

        if args.lossy:
            convert_sequence.compress_gif(args.lossy)

def parse_args():

    parser = argparse.ArgumentParser(description='Converts video/sequence to GIF')
    parser.add_argument('-i', '--input', type=str, metavar='', help='Input file path', required=True)

    parser.add_argument('-w', '--no-transparent', action='store_false', help='Disable transparency', required=False)
    parser.add_argument('-l', '--lossy', type=str, default=None, metavar='', help='No. of artefacts allowed', required=False)
    parser.add_argument('-z', '--optimise', type=int, default=None, metavar='', help='Optimise GIF file size (1 - 3)', required=False)
    
    parser.add_argument('-a', '--assemble', action='store_true', help='Assemble image sequence', required=False)
    parser.add_argument('-r', '--fps', type=int, default=50, metavar='', help='Sequence FPS', required=False)

    return parser.parse_known_args()

if __name__ == '__main__':
    args, _ = parse_args()
    main(args)