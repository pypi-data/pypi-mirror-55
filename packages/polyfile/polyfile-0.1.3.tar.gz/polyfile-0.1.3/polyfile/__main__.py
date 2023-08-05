import argparse
import json
import logging
import sys

from . import html
from . import logger
from . import polyfile
from . import version
from .fileutils import PathOrStdin


log = logger.getStatusLogger("polyfile")


def main(argv=None):
    parser = argparse.ArgumentParser(description='A utility to recursively map the structure of a file.')
    parser.add_argument('FILE', nargs='?', default='-', help='The file to analyze; pass \'-\' or omit to read from STDIN')
    parser.add_argument('--html', '-t', type=argparse.FileType('wb'), required=False,
                        help='Path to write an interactive HTML file for exploring the PDF')
    parser.add_argument('--try-all-offsets', '-a', action='store_true', help='Search for a file match at every possible offset; this can be very slow for larger files')
    parser.add_argument('--debug', '-d', action='store_true', help='Print debug information')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress all log output (overrides --debug)')
    parser.add_argument('--version', '-v', action='store_true', help='Print PolyFile\'s version information to STDERR')
    parser.add_argument('-dumpversion', action='store_true', help='Print PolyFile\'s raw version information to STDOUT and exit')

    if argv is None:
        argv = sys.argv
    
    args = parser.parse_args(argv[1:])

    if args.dumpversion:
        print(' '.join(map(str, version.__version__)))
        exit(0)

    if args.version:
        sys.stderr.write(f"PolyFile version {version.VERSION_STRING}\n")
        if args.FILE == '-' and sys.stdin.isatty():
            # No file argument was provided and it doesn't look like anything was piped into STDIN,
            # so instead of blocking on STDIN just exit
            exit(0)

    if args.debug:
        logger.setLevel(logging.DEBUG)
    elif args.quiet:
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logger.STATUS)

    if args.quiet:
        progress_callback = None
    else:
        class ProgressCallback:
            def __init__(self):
                self.last_percent = -1

            def __call__(self, pos, length):
                if length == 0:
                    percent = 0.0
                else:
                    percent = int(pos / length * 10000.0) / 100.0

                if percent > self.last_percent:
                    log.status(f"{percent:.2f}% {pos}/{length}")
                    self.last_percent = percent

        progress_callback = ProgressCallback()

    with PathOrStdin(args.FILE) as file_path:
        matches = []
        matcher = polyfile.Matcher(args.try_all_offsets)
        for match in matcher.match(file_path, progress_callback=progress_callback):
            if hasattr(match.match, 'filetype'):
                filetype = match.match.filetype
            else:
                filetype = match.name
            if match.parent is None:
                log.info(f"Found a file of type {filetype} at byte offset {match.offset}")
                matches.append(match)
            elif isinstance(match, polyfile.Submatch):
                log.info(f"Found a subregion of type {filetype} at byte offset {match.offset}")
            else:
                log.info(f"Found an embedded file of type {filetype} at byte offset {match.offset}")
        sys.stderr.flush()
        matches = [match.to_obj() for match in matches]
        print(json.dumps(matches))
        if args.html:
            args.html.write(html.generate(file_path, matches).encode('utf-8'))
            args.html.close()
            log.info(f"Saved HTML output to {args.html.name}")


if __name__ == '__main__':
    main()
