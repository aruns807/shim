# Routes keyboard input to appropriate interaction manager
# to mutate instance state page is then re-rendered given new state
# Events are fed directly from user_input
# Interaction manager should not have to parse user input keys directly
import sys
from backend.interaction_managers import (
    cursor_logic, text_logic, graphics_logic)


def render_default_graphics(graphics_state, local_state, global_state):
    """
    Render 'default' graphics i.e line numbers, cursor, text lines etc.
    """
    lines = local_state.get_line_tokens()
    x, y, curr_top = local_state.get_page_state()
    buff_line_count = graphics_state.get_line_height()

    graphics_state.draw_cursor(x, y)
    graphics_state.draw_line_numbers(curr_top + 1)
    for i in range(buff_line_count + 1):
        try:
            graphics_state.write_line_grid(i, lines[curr_top + i])
        except IndexError:
            break
    x, y, t = local_state.get_page_state()
    status_line = 'file: %s  |  mode: %s  |  %d, %d | command buffer: %s' % \
        (local_state.get_filename(), global_state.get_curr_state(), x, y + t,
            global_state.get_command_buffer())
    graphics_state.write_status_line(status_line)


def render_page(graphics_state, local_state, global_state, pre=[], post=[]):
    """
    Clear buffer and and run pre and post graphics mutating functions
    Pre and post should contain a list of lambdas like so:
    [lambda: graphics_logic.highlight_visual_mode(graphics_state, local_state)]
    That way graphics can be rendered both before and after the default
    rendering routine is called so as to allow for flexibility with plugins and
    default rendering functions
    """
    graphics_state.clear_all()
    for func in pre:
        func()
    render_default_graphics(graphics_state, local_state, global_state)
    for func in post:
        func()


def move_left(graphics_state, local_state, global_state):
    """
    Functionality corresponding to h in vim
    """
    cursor_logic.move_cursor_left(local_state)
    render_page(graphics_state, local_state, global_state)


def move_right(graphics_state, local_state, global_state):
    """
    Functionality corresponding to l in vim
    """
    cursor_logic.move_cursor_right(local_state)
    render_page(graphics_state, local_state, global_state)


def move_down(graphics_state, local_state, global_state):
    """
    Functionality corresponding to j in vim
    """
    cursor_logic.move_cursor_down(local_state)
    render_page(graphics_state, local_state, global_state)


def move_up(graphics_state, local_state, global_state):
    """
    Functionality corresponding to k in vim
    """
    cursor_logic.move_cursor_up(local_state)
    render_page(graphics_state, local_state, global_state)


def move_beginning_line(graphics_state, local_state, global_state):
    """
    Functionality corresponding to 0 in vim
    """
    cursor_logic.move_cursor_beginning_line(local_state)
    render_page(graphics_state, local_state, global_state)


def move_end_line(graphics_state, local_state, global_state):
    """
    Functionality corresponding to $ in vim
    """
    cursor_logic.move_cursor_end_line(local_state)
    render_page(graphics_state, local_state, global_state)


def move_next_word_front(graphics_state, local_state, global_state):
    """
    Functionality corresponding to w in vim
    """
    cursor_logic.move_cursor_next_word_front(local_state)
    render_page(graphics_state, local_state, global_state)


def move_next_word_end(graphics_state, local_state, global_state):
    """
    Functionality corresponding to e in vim
    """
    cursor_logic.move_cursor_next_word_end(local_state)
    render_page(graphics_state, local_state, global_state)


def move_prev_word_front(graphics_state, local_state, global_state):
    """
    Functionality corresponding to b in vim
    """
    cursor_logic.move_cursor_move_prev_word_front(local_state)
    render_page(graphics_state, local_state, global_state)


def move_end_file(graphics_state, local_state, global_state):
    """
    Functionality corresponding to G in vim
    """
    cursor_logic.move_cursor_end_file(local_state)
    render_page(graphics_state, local_state, global_state)


def move_begin_file(graphics_state, local_state, global_state):
    """
    Functionality corresponding to gg in vim
    """
    cursor_logic.move_cursor_begin_file(local_state)
    render_page(graphics_state, local_state, global_state)


def move_next_paragraph(graphics_state, local_state, global_state):
    """
    Functionality corresponding to } in vim
    """
    cursor_logic.move_cursor_next_paragraph(local_state)
    render_page(graphics_state, local_state, global_state)


def move_prev_paragraph(graphics_state, local_state, global_state):
    """
    Functionality corresponding to { in vim
    """
    cursor_logic.move_cursor_prev_paragraph(local_state)
    render_page(graphics_state, local_state, global_state)


def move_line_num(n_arg, graphics_state, local_state, global_state):
    """
    Functionality corresponding to line number jumps in vim
    i.e 123gg jumps to line 123
    """
    cursor_logic.move_cursor_line_num(n_arg, local_state)
    render_page(graphics_state, local_state, global_state)


def move_seek_char(c_arg, graphics_state, local_state, global_state):
    """
    Functionality corresponding to f[character] in vim
    """
    cursor_logic.move_cursor_seek_char(c_arg, local_state)
    render_page(graphics_state, local_state, global_state)


def insert_text(s_arg, graphics_state, local_state, global_state):
    text_logic.insert_text_str(s_arg, local_state)
    render_page(graphics_state, local_state, global_state)


def delete_char(graphics_state, local_state, global_state):
    """
    Functionality corresponding to x in vim
    """
    text_logic.delete_text_char(local_state)
    render_page(graphics_state, local_state, global_state)


def add_new_line(graphics_state, local_state, global_state):
    """
    Functionality corresponding to <Return> in vim
    """
    text_logic.add_new_line_char(local_state)
    render_page(graphics_state, local_state, global_state)


def delete_text_movement(movement, graphics_state, local_state, global_state):
    """
    Delete a text in a given range. I.e 'dw' or 'd}'
    Performs this operation by:
        1. Getting current location
        2. Mutating page state with movement argument
        3. Getting location after page manipulation
        4. Mutating local line buffer to remove desired range

    TODO: This is not optimal,
    Calling COMMAND_MAP[movement](graphics_state, local_state, global_state)
    messes with graphics state unnecessarily
    """
    px, py, pt = local_state.get_page_state()
    COMMAND_MAP[movement](graphics_state, local_state, global_state)
    nx, ny, nt = local_state.get_page_state()

    text_logic.delete_text_range(px, py, pt, nx, ny, nt, local_state)
    render_page(graphics_state, local_state, global_state)


def delete_text_highlight(graphics_state, local_state, global_state):
    """
    Delete text under highlight.
    Cursor corresponds to a highlight over a single character
    i.e Calling delete_text_highlight without visual mode on corresponds to
    deleting a single character or x in vim
    TODO: In the visual mode case this adds the deleted text to the copy buffer
    This should be mirrored in the non visual mode case
    """
    if global_state.get_curr_state() == 'Visual':
        px, py, pt = local_state.get_visual_anchors()
        nx, ny, nt = local_state.get_page_state()
        txt = text_logic.get_text_range(px, py, pt, nx, ny, nt, local_state)
        global_state.add_copy_buffer(txt)
        text_logic.delete_text_range(px, py, pt, nx, ny, nt, local_state)
        global_state.set_curr_state('Default')
    else:
        text_logic.delete_text_highlight(local_state)

    render_page(graphics_state, local_state, global_state)


def delete_curr_line(graphics_state, local_state, global_state):
    """
    Functionality corresponding to dd in vim
    """
    text_logic.delete_current_line(local_state, global_state)
    render_page(graphics_state, local_state, global_state)


def insert_new_line_above(graphics_state, local_state, global_state):
    """
    Functionality corresponding to O in vim
    """
    global_state.set_curr_state('Insert')
    text_logic.insert_new_line_above(local_state)
    render_page(graphics_state, local_state, global_state)


def insert_new_line_below(graphics_state, local_state, global_state):
    """
    Functionality corresponding to o in vim
    """
    global_state.set_curr_state('Insert')
    text_logic.insert_new_line_below(local_state)
    render_page(graphics_state, local_state, global_state)


def insert_end_of_line(graphics_state, local_state, global_state):
    """
    Functionality corresponding to A in vim
    """
    global_state.set_curr_state('Insert')
    cursor_logic.move_cursor_past_end_line(local_state)
    render_page(graphics_state, local_state, global_state)


def mouse_scroll(delta, graphics_state, local_state, global_state):
    """
    Moves cursor upward to downward depending on scroll direction
    TODO: Similarly, a mouse click should move the cursor to the x, y location
    of the mouse
    """
    x, y, curr_top = local_state.get_page_state()
    if y + int(delta) + curr_top <= local_state.get_line_num() - 2:
        local_state.set_cursor(x, y + int(delta))
        render_page(graphics_state, local_state, global_state)
    else:
        move_end_file(graphics_state, local_state, global_state)


def visual_movement(motion, graphics_state, local_state, global_state):
    """
    Movement in visual mode, render line highlight code in prior to
    'Default' graphics rendering routine
    """
    COMMAND_MAP[motion](graphics_state, local_state, global_state)
    # some commands break out of visual mode
    if global_state.get_curr_state() == 'Visual':
        f = lambda: graphics_logic.highlight_visual_mode(
            graphics_state, local_state
        )
        render_page(graphics_state, local_state, global_state, post=[f])


def paste(graphics_state, local_state, global_state):
    """
    Functionality corresponding to p in vim
    """
    text_logic.insert_copy_buffer(local_state, global_state)
    render_page(graphics_state, local_state, global_state)


def yank_curr_line(graphics_state, local_state, global_state):
    """
    Functionality corresponding to yy in vim
    """
    x, y, curr_top = local_state.get_page_state()
    global_state.add_copy_buffer([local_state.get_line(curr_top + y)])


def shift_selection_right(graphics_state, local_state, global_state):
    """
    Functionality that closely mirrors > in vim
    Does not exist visual mode on shift completion
    TODO: Discuss whether or not it should remain that way
    """
    text_logic.shift_selection_right(local_state)
    render_page(graphics_state, local_state, global_state)


def shift_selection_left(graphics_state, local_state, global_state):
    """
    Functionality that closely mirrors < in vim
    Does not exist visual mode on shift completion
    TODO: Discuss whether or not it should remain that way
    """
    text_logic.shift_selection_left(local_state)
    render_page(graphics_state, local_state, global_state)


def quit(graphics_state, local_state, global_state):
    """
    Quit shim.
    Add shutdown routines here if need be
    """
    sys.exit(1)


def write(graphics_state, local_state, global_state):
    lines = ''.join(local_state.get_lines())
    with open(local_state.get_filename(), 'w') as f:
        f.write(lines)


def write_and_quit(graphics_state, local_state, global_state):
    write(graphics_state, local_state, global_state)
    quit(graphics_state, local_state, global_state)


def undo_command(graphics_state, local_state, global_state):
    """
    Functionality corresponding to u in vim
    """
    local_state.undo_state()
    render_page(graphics_state, local_state, global_state)


def redo_command(graphics_state, local_state, global_state):
    """
    Functionality corresponding to <Control-r> in vim
    """
    local_state.redo_state()
    render_page(graphics_state, local_state, global_state)


def move_next_instance_buffer(graphics_state, local_state, global_state):
    """
    Functionality corresponding to :bn in vim
    Currently bound to <Control-}>
    """
    global_state.go_next_instance()


def move_prev_instance_buffer(graphics_state, local_state, global_state):
    """
    Functionality corresponding to :bp in vim
    Currently bound to <Control-{>
    """
    global_state.go_prev_instance()


def visual_yank(graphics_state, local_state, global_state):
    """
    Place in copy buffer the text
    currently selected under visual mode
    """
    px, py, pt = local_state.get_visual_anchors()
    nx, ny, nt = local_state.get_page_state()
    txt = text_logic.get_text_range(px, py, pt, nx, ny, nt, local_state)
    global_state.add_copy_buffer(txt)
    global_state.set_curr_state('Default')
    render_page(graphics_state, local_state, global_state)


COMMAND_MAP = {
    'quit': quit,
    'write': write,
    'paste': paste,
    'move_cursor_up': move_up,
    'insert_text': insert_text,
    'delete_char': delete_char,
    'visual_yank': visual_yank,
    'undo_command': undo_command,
    'redo_command': redo_command,
    'mouse_scroll': mouse_scroll,
    'add_new_line': add_new_line,
    'move_cursor_left': move_left,
    'move_cursor_down': move_down,
    'move_cursor_right': move_right,
    'write_and_quit': write_and_quit,
    'yank_curr_line': yank_curr_line,
    'visual_movement': visual_movement,
    'delete_curr_line': delete_curr_line,
    'move_cursor_end_line': move_end_line,
    'move_cursor_end_file': move_end_file,
    'move_cursor_line_num': move_line_num,
    'move_cursor_seek_char': move_seek_char,
    'insert_end_of_line': insert_end_of_line,
    'move_cursor_begin_file': move_begin_file,
    'shift_selection_left': shift_selection_left,
    'delete_text_movement': delete_text_movement,
    'insert_new_line_above': insert_new_line_above,
    'insert_new_line_below': insert_new_line_below,
    'delete_text_highlight': delete_text_highlight,
    'shift_selection_right': shift_selection_right,
    'move_cursor_next_word_end': move_next_word_end,
    'move_cursor_next_paragraph': move_next_paragraph,
    'move_cursor_prev_paragraph': move_prev_paragraph,
    'move_cursor_beginning_line': move_beginning_line,
    'move_cursor_next_word_front': move_next_word_front,
    'move_cursor_prev_word_front': move_prev_word_front,
    'move_next_instance_buffer': move_next_instance_buffer,
    'move_prev_instance_buffer': move_prev_instance_buffer,
}


def input_command(command, graphics_state, local_state, global_state):
    """
    Look up mapping for appropriate function to call
    if multiple commands are passed in, separate parsing logic is required
    """
    if len(command) == 1:
        COMMAND_MAP[command[0]](graphics_state, local_state, global_state)
    else:
        input_command_arg(command, graphics_state, local_state, global_state)


def input_command_arg(commands, graphics_state, local_state, global_state):
    """
    Logic to handle commands that are not singular i.e f[char] or d}

    TODO: These mapping schemes might not be valid anymore once a proper
    parser is implemented
    c denotes character arguments i.e fa maps to find a
    n denotes numerical arguments i.e 123gg maps to jump to line 123
    r denotes repeat arguments i.e 3j means run the 'j' command 3 times
    s denotes character arguments i.e text insert
    """
    opt_arg = commands[0][1:]
    in_arg = commands[1]
    if commands[0].startswith('n'):
        COMMAND_MAP[in_arg](
            int(opt_arg), graphics_state, local_state, global_state)
    elif commands[0].startswith('r'):
        for i in range(int(opt_arg)):
            COMMAND_MAP[in_arg](graphics_state, local_state, global_state)
    elif commands[0].startswith('c'):
        # This should be a single character argument anyway
        COMMAND_MAP[in_arg](opt_arg, graphics_state, local_state, global_state)
    elif commands[0].startswith('s'):
        COMMAND_MAP[in_arg](opt_arg, graphics_state, local_state, global_state)
