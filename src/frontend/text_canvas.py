# Main class for handling graphics
# all api's related to graphics should be called
# from this class
# TODO: Discuss what kind of functions this class
# should provide

from tkinter import Canvas, BOTH
from tkinter.ttk import Frame
import tkinter.font as tkFont
from backend.state.syntaxtokens.color_config import options


class text_canvas(Frame):

    def __init__(self, parent, font_size, input_handler, filename):
        Frame.__init__(self, parent)
        self._parent = parent
        self._text_font = tkFont.Font(
            family='Monaco', size=font_size, weight='bold'
        )
        self._filename = filename
        self._cheight, self._cwidth = font_size, self._text_font.measure('c')
        self._line_num_spacing = (self.get_num_spacing() * self._cwidth) + 20
        self._line_height = (
            (self.winfo_screenheight() - self._cheight)//(self._cheight + 2) - 4
        )
        self.init_UI(input_handler)

    def init_UI(self, input_handler):
        self._parent.title('')
        self.pack(fill=BOTH, expand=1)
        self.init_canvas(input_handler)

    def get_dimensions(self):
        """
        Getting the dimensions might be helpful
        for plugin writers
        """
        return {
            'cheight': self._cheight,
            'cwidth': self._cwidth,
            'line_num_spacing': self._line_num_spacing,
            'line_height': self._line_height,
            'screen_width': self.winfo_screenwidth(),
            'screen_height': self.winfo_screenheight()
        }

    def get_num_spacing(self):
        n = sum(1 for line in open(self._filename))
        return len(str(n))

    def get_line_height(self):
        return self._line_height

    def init_canvas(self, input_handler):
        self._canvas = Canvas(
            self, highlightthickness=0, width=self.winfo_screenwidth(),
            height=self.winfo_screenheight(), bg=options['background_color']
        )
        self._canvas.pack()
        self._canvas.focus_set()
        self.bind_events(input_handler)

    def clear_all(self):
        self._canvas.delete('all')

    def get_line_height(self):
        """
        return number of lines per page
        """
        return self._line_height

    def get_grid_y(self, y):
        """
        return character height * y
        in addition distane of the spaces inbetwen
        """
        return self._cheight * y + (y * 2)

    def write_line_grid(self, y, line):
        """
        Write to line of text on grid using tokens passed in
        """
        for token in line:
            self.write_text_grid(token[0], y, token[1], token[2])

    def write_text_grid(self, x, y, text, color=options['text_color']):
        """
        Write text to x, y location on grid
        """
        x_val = self._cwidth * x + self._line_num_spacing
        y_val = self._cheight * y + (y * 2)  # 2 pixel spacing between each line
        self._canvas.create_text(
            x_val, y_val, anchor='nw', text=text,
            font=self._text_font, fill=color
        )

    def write_status_line(
        self, text, textcolor=options['status_text_color'],
        backgroundcolor=options['status_background_color']
    ):
        """
        Writen a line of text to status line
        this function could take in different data if desired
        """
        y = self._line_height + 1
        self._canvas.create_rectangle(
            0, self._cheight * y + (y * 2), self.winfo_screenwidth(),
            self._cheight * y + (y * 2) + self._cheight + 4,
            fill=backgroundcolor, outline=backgroundcolor
        )
        self.write_text_grid(0, self._line_height + 1, text, textcolor)

    def draw_highlight_grid(
        self, y, x1, x2,
        highlightcolor=options['text_highlight_color']
    ):
        """
        Draw highlights onto text canvas
        i.e selections during visual mode
        """
        y_val = self._cheight * y + (y * 2)
        x1_val = self._cwidth * x1 + self._line_num_spacing
        x2_val = self._cwidth * x2 + self._line_num_spacing
        self._canvas.create_rectangle(
            x1_val, y_val, x2_val, y_val + self._cheight + 4,
            fill=highlightcolor, outline=highlightcolor
        )

    def draw_line_numbers(
        self, start,
        highlightcolor=options['line_num_highlight_color'],
        textcolor=options['line_num_text_color']
    ):
        self._canvas.create_rectangle(
            0, 0, self._line_num_spacing - 20,
            self.winfo_screenheight(),
            fill=highlightcolor, outline=highlightcolor
        )
        for i in range(self._line_height + 1):
            self._canvas.create_text(
                0, self._cheight * i + (i * 2), anchor='nw',
                text=str(start + i), font=self._text_font,
                fill=textcolor
            )

    def draw_cursor(
        self, x, y,
        highlightcolor=options['cursor_highlight_color'],
        cursorcolor=options['cursor_color']
    ):
        """
        draw cursor as well as line and column highlights
        TODO: users should have the option to disable line
        and column highlights
        """
        x_val = self._cwidth * x + self._line_num_spacing
        y_val = self._cheight * y + (y * 2)

        self._canvas.create_rectangle(
            0, y_val, self.winfo_screenwidth(),
            y_val + self._cheight + 4,
            fill=highlightcolor, outline=highlightcolor
        )
        self._canvas.create_rectangle(
            x_val, 0, x_val + self._cwidth,
            self.winfo_screenheight(), fill=highlightcolor,
            outline=highlightcolor
        )
        self._canvas.create_rectangle(
            x_val, y_val, x_val + self._cwidth,
            y_val + self._cheight + 4,
            fill=cursorcolor, outline=cursorcolor
        )

    def draw_rectangle_absolute(
        self, x1, y1, x2, y2, color
    ):
        """
        draw rectangle onto screen
        TODO: flesh out what this function should actually
        look like
        """
        self._canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color, outline=color
        )

    def bind_events(self, input_handler):
        """
        bind events for use in input_handler
        TODO: this should be cleaned up ideally into a separate handler list
        """
        input_handler.set_GUI_reference(self)
        self._canvas.bind('<Key>', input_handler.key)
        self._canvas.bind_all('<Escape>', input_handler.escape)
        self._canvas.bind_all('<Control-a>', input_handler.control_a)
        self._canvas.bind_all('<Control-b>', input_handler.control_b)
        self._canvas.bind_all('<Control-c>', input_handler.control_c)
        self._canvas.bind_all('<Control-d>', input_handler.control_d)
        self._canvas.bind_all('<Control-e>', input_handler.control_e)
        self._canvas.bind_all('<Control-f>', input_handler.control_f)
        self._canvas.bind_all('<Control-g>', input_handler.control_g)
        self._canvas.bind_all('<Control-h>', input_handler.control_h)
        self._canvas.bind_all('<Control-i>', input_handler.control_i)
        self._canvas.bind_all('<Control-j>', input_handler.control_j)
        self._canvas.bind_all('<Control-k>', input_handler.control_k)
        self._canvas.bind_all('<Control-l>', input_handler.control_l)
        self._canvas.bind_all('<Control-m>', input_handler.control_m)
        self._canvas.bind_all('<Control-n>', input_handler.control_n)
        self._canvas.bind_all('<Control-o>', input_handler.control_o)
        self._canvas.bind_all('<Control-p>', input_handler.control_p)
        self._canvas.bind_all('<Control-q>', input_handler.control_q)
        self._canvas.bind_all('<Control-r>', input_handler.control_r)
        self._canvas.bind_all('<Control-s>', input_handler.control_s)
        self._canvas.bind_all('<Control-t>', input_handler.control_t)
        self._canvas.bind_all('<Control-u>', input_handler.control_u)
        self._canvas.bind_all('<Control-v>', input_handler.control_v)
        self._canvas.bind_all('<Control-w>', input_handler.control_w)
        self._canvas.bind_all('<Control-x>', input_handler.control_x)
        self._canvas.bind_all('<Control-y>', input_handler.control_y)
        self._canvas.bind_all('<Control-z>', input_handler.control_z)
        self._canvas.bind_all("<MouseWheel>", input_handler.mouse_scroll)
        self._canvas.bind_all(
            '<Control-braceright>', input_handler.control_braceright
        )
        self._canvas.bind_all(
            '<Control-braceleft>', input_handler.control_braceleft
        )
