#!/usr/bin/python
from Tkinter import Tk, Image
from Frontend import text_canvas
from Backend import user_input
from optparse import OptionParser
from os import path
import metadata

parser = OptionParser()

def opt_init():
    parser.add_option('-m', '--load_meta_data', dest='load_meta_data',
                      action='store_true', default=False, help='Run meta data loader')


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
    opt_init()
    (options, args) = parser.parse_args()

    if options.load_meta_data:
        print 'CREATING META DATA FILES'
        metadata.create_metadata_files()
    else:
        if not path.isfile('.shimdata'):
            print 'META DATA FILE DOES NOT EXIST YET'
            print 'GENERATING META DATA FILES'
            metadata.create_metadata_files()
        try:
            run_text_editor(args[0])
        except IndexError:
            print 'failure! Did not specify file to edit'
