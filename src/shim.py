#!/usr/bin/env python3
from tkinter import Tk, Image
from argparse import ArgumentParser
from frontend import text_canvas
from backend import user_input

def opt_init():
    parser = ArgumentParser(description='A vim inspired text editor')
    parser.add_argument(dest='filename', action='store', metavar='FILE', nargs='?')
    parser.add_argument('-v', '--version', action='version', version='/dev/null')
    return parser

def run_text_editor(filename):
    root = Tk()
    input_handler = user_input.user_input()

    input_handler.start_instance(filename)
    app = text_canvas.text_canvas(root, 12, input_handler, filename)

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
