#!/usr/bin/env python3
from tkinter import Tk
from argparse import ArgumentParser
from Frontend import text_canvas
from Backend import user_input


def opt_init():
    """To parse option command line"""
    parser = ArgumentParser(description='A vim inspired text editor')
    parser.add_argument(dest='filename', action='store',
                        metavar='FILE', nargs='?')
    parser.add_argument('-v', '--version',
                        action='version', version='/dev/null')
    return parser


def run_text_editor(filename):
    """To run text editor"""
    root = Tk()
    input_handler = user_input.user_input()

    input_handler.start_instance(filename)
    text_canvas.text_canvas(root, 12, input_handler, filename)

    root.wm_attributes('-fullscreen', 1)
    root.title('shim')
    root.overrideredirect()

    root.mainloop()


if __name__ == '__main__':
    parser = opt_init()
    args = parser.parse_args()

    if args.filename:
        run_text_editor(args.filename)
    else:
        parser.print_usage()
