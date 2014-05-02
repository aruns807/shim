# dump all pygments tokens into a text file to determine
# how pygments assigns tokens to various files

from pygments import lex
from pygments.lexers import get_lexer_for_filename
from pygments.token import Token

from argparse import ArgumentParser


def opt_init():
    """To parse option command line"""
    parser = ArgumentParser(description='token dump test')
    parser.add_argument(dest='filename', action='store',
                        metavar='FILE', nargs='?')
    parser.add_argument(
        '-out', dest='out', nargs='?',
        default=None
    )
    return parser

if __name__ == '__main__':
    parser = opt_init()
    args = parser.parse_args()
    if args.filename:
        filename = args.filename
        lexer = get_lexer_for_filename(filename)
        out = ''

        txt = open(filename, 'r').read()
        for token in lex(txt, lexer):
            out += str(token) + '\n'

        if args.out:
            with open(args.out, 'w') as f:
                f.write(out)
                print('token dump located at %s' % (args.out))
        else:
            print(out)
    else:
        print('missing filename argument')
