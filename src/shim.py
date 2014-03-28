#!/usr/bin/python
from Tkinter import Tk, Image
from Frontend import text_canvas
from Backend import user_input
from argparse import ArgumentParser
import loader, metadata, os.path, sys

def opt_init():
    parser = ArgumentParser(description='A vim inspired text editor for all')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(dest='filename', action='store', metavar='FILE', nargs='?')
    group.add_argument('-m', '--load-meta-data', dest='load_meta_data',
                      action='store_true', default=False, help='Run meta data loader')
    group.add_argument('-l', '--load-plugins', dest='load_plugins', metavar='PATH',
                      action='store', default=None, help='Run plugin loader with directory name')
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

    if args.load_plugins != None:
        print 'LOADING PLUGIN CODE'
        loader.load_plugin(args.load_plugins)
    
    elif args.load_meta_data:
        print 'CREATING META DATA FILES'
        metadata.create_metadata_files()
    else:
        if not os.path.isfile('.shimdata'):
            print 'META DATA FILE DOES NOT EXIST YET'
            print 'GENERATING META DATA FILES'
            metadata.create_metadata_files()

        if args.filename:
            run_text_editor(args.filename)
        else:
            parser.print_usage()
