
from argparse import ArgumentParser, Namespace
from libs.convert_video import ConvertVideo
from libs.convert_sequence import ConvertSequence

def generate_gif(convert: ConvertSequence | ConvertVideo, args: Namespace):

    (
        convert.generate_palette()
               .to_gif()
               .clear_temp_files()
    )

    if args.optimise:
        convert.optimize_gif(args.optimise)

    if args.lossy:
        convert.compress_gif(args.lossy)

    convert.print_output_info()

def main():

    args, _ = parse_args()

    if not args.assemble:
        convert = ConvertVideo(args.input, args.transparent)

    else:
        convert = ConvertSequence(args.input, args.transparent, args.fps)

    generate_gif(convert, args)

def parse_args() -> tuple[Namespace, list[str]]:

    parser = ArgumentParser(description='Converts video/sequence to GIF')
    parser.add_argument('-i', '--input', type=str, metavar='', help='Input file path', required=True)

    parser.add_argument('-w', '--transparent', action='store_true', help='Enable transparency', required=False)
    parser.add_argument('-l', '--lossy', type=str, default=None, metavar='', help='No. of artefacts allowed', required=False)
    parser.add_argument('-z', '--optimise', type=int, default=None, metavar='', help='Optimise GIF file size (1 - 3)', required=False)
    
    parser.add_argument('-a', '--assemble', action='store_true', help='Assemble image sequence', required=False)
    parser.add_argument('-r', '--fps', type=int, default=50, metavar='', help='Sequence FPS', required=False)

    return parser.parse_known_args()

if __name__ == '__main__':
    main()
