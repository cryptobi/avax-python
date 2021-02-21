"""CB58 encode or decode FILE, or standard input, to standard output.
"""
import argparse
import sys

from . import __version__, cb58decode, cb58encode


EPILOG = """
CB58 is a base-58 encoding with a 32-bit checksum, used on the AVA network.
It's similar to base58check.
"""


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='cb58ref',
        description=__doc__,
        epilog=EPILOG,
    )
    parser.add_argument(
        '-d', '--decode', action='store_true',
        help='decode data',
    )
    parser.add_argument(
        '-n', action='store_false',
        dest='newline',
        help='do not output the trailing newline',
    )
    parser.add_argument(
        'file', metavar='FILE',
        type=argparse.FileType('rb'),
        default='-',
        nargs='?',
        help='file to read from (default: stdin)'
    )
    parser.add_argument(
        '--version', action='store_true',
        help='print program version and exit',
    )
    args = parser.parse_args(argv)

    if args.version:
        print(parser.prog, __version__)
        return 0

    # Workaround for https://bugs.python.org/issue14156
    # We want to read binary data, but (as of Jun 2020) argparse doesn't
    # provide that when reading from stdin.
    if args.file == sys.stdin:
        args.file = args.file.buffer

    # Read CB58, output bytes
    if args.decode:
        s = args.file.read().decode('ascii')
        b = cb58decode(s)
        sys.stdout.buffer.write(b)
        if args.newline:
            sys.stdout.buffer.write(b'\n')
        return 0

    # Read CB58, output CB58
    b = args.file.read()
    s = cb58encode(b)
    sys.stdout.write(s)
    if args.newline:
        sys.stdout.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
