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
    return parser

if __name__ == '__main__':
    parser = opt_init()
    args = parser.parse_args()
    if args.filename:
        filename = args.filename
        lexer = get_lexer_for_filename(filename)

        with open('token.out', 'w') as f:
            txt = open(filename, 'r').read()
            for token in lex(txt, lexer):
                f.write(str(token) + '\n')
        print('token dump located at token.out')
    else:
        print('missing filename argument')
