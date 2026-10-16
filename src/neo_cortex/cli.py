import sys

from . import __version__


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if args[:1] == ["--version"]:
        print(__version__)
        return 0
    print("neo: not implemented yet (try --version)")
    return 0
