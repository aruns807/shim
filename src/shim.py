#!/usr/bin/python
from Tkinter import Tk, Image
from Frontend import text_canvas
from Backend import user_input
from optparse import OptionParser
from os import path

parser = OptionParser()

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
    (options, args) = parser.parse_args()

    try:
        run_text_editor(args[0])
    except IndexError:
        print 'failure! Did not specify file to edit'
