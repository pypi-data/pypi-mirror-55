from . import *
import sys

def main():
    argv, arglen = sys.argv, len(sys.argv)
    first = argv[1] if arglen > 1 else ''
    argv = argv[2:] if arglen > 2 else []

    if first == '-s' or (first == 'srt'):
        srt.srt(argv)
    elif first == '-y' or (first == 'yml'):
        yml.yml(argv)
    elif first == '-m' or (first == 'md'):
        markdown.markdown(argv)
    elif first == '-l' or (first == 'ls'):
        ls.ls(argv)
    else:
        print("udt-cli v{}".format(__version__))
