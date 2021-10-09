import argparse

from libs.convert_video import ConvertVideo
from libs.convert_sequence import ConvertSequence

def main(args):

    if args.convert_type == 'vid':
        convert_video = ConvertVideo(args.input)
        convert_video.generate_palette(args.no_transparent)
        convert_video.to_gif()
        convert_video.clear_temp_files()
        convert_video.print_output_info()

    elif args.convert_type == 'seq':
        convert_sequence = ConvertSequence(args.input, args.fps)
        convert_sequence.to_gif()

def parse_args():

    parser = argparse.ArgumentParser(description='Converts video/sequence to GIF')
    parser.add_argument('-i', '--input', type=str, metavar='', help='Input file path', required=True)

    subparser = parser.add_subparsers(dest='convert_type')

    video_parser = subparser.add_parser('vid', help="Converts video to GIF")
    video_parser.add_argument('-w', '--no-transparent', action='store_false', help='Disable transparency', required=False)
    video_parser.add_argument('-l', '--lossy', type=int, default=None, metavar='', help='No. of artifacts allowed', required=False)
    video_parser.add_argument('-z', '--optimise', type=int, default=None, metavar='', help='Optimise GIF file size (1 - 3)', required=False)
    
    sequence_parser = subparser.add_parser('seq', help="Converts sequence to GIF")
    sequence_parser.add_argument('-r', '--fps', type=int, default=50, metavar='', help='Sequence FPS', required=False)

    return parser.parse_known_args()

if __name__ == '__main__':
    args, _ = parse_args()
    main(args)