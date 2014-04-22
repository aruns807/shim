from backend.interaction_managers import cursor_logic
from backend.command_list import COMMAND_MAP as c_map


def insert_text_str(s, local_state):
    """
    Insert string into line
    """
    x, y, curr_top = local_state.get_page_state()
    curr_line = local_state.get_line(curr_top + y)
    local_state.set_line(curr_top + y, curr_line[:x] + s + curr_line[x:])
    local_state.set_cursor(x + len(s), y)


def insert_copy_buffer(local_state, global_state):
    """
    Insert multiple strings into line start at
    curr_top + y
    """
    x, y, curr_top = local_state.get_page_state()
    paste_txt = global_state.get_copy_buffer()

    if len(paste_txt):
        curr_line = local_state.get_line(curr_top + y)
        local_state.set_line(
            curr_top + y,
            curr_line[:x] + paste_txt[0].strip('\n') + curr_line[x:]
        )
        for i in range(len(paste_txt) - 1):
            local_state.add_line(curr_top + y + i + 1, paste_txt[i + 1])


def delete_text_highlight(local_state):
    """
    Splice out a single character from a line
    """
    x, y, curr_top = local_state.get_page_state()
    curr_line = local_state.get_line(curr_top + y)
    local_state.set_line(curr_top + y, curr_line[:x] + curr_line[x + 1:])


def delete_current_line(local_state, global_state):
    """
    Functionality corresponding to dd in vim
    """
    x, y, curr_top = local_state.get_page_state()
    global_state.add_copy_buffer(
        [local_state.get_line(curr_top + y)]
    )
    local_state.remove_line(curr_top + y)
    local_state.set_cursor(0, y)


def insert_new_line_below(local_state):
    """
    Functionality corresponding to o in vim
    adds whitespace as well as newline character to
    match indent level of 'source' line
    """
    x, y, curr_top = local_state.get_page_state()
    curr_line = local_state.get_line(curr_top + y)

    new_line = (' ' * (len(curr_line) - len(curr_line.lstrip()))) + '\n'
    local_state.add_line(y + curr_top + 1, new_line)
    local_state.set_cursor(len(curr_line) - len(curr_line.lstrip()), y + 1)


def insert_new_line_above(local_state):
    """
    Functionality corresponding to O in vim
    adds whitespace as well as newline character to
    match indent level of 'source' line
    """
    x, y, curr_top = local_state.get_page_state()
    curr_line = local_state.get_line(curr_top + y)

    new_line = (' ' * (len(curr_line) - len(curr_line.lstrip()))) + '\n'
    local_state.add_line(y + curr_top, new_line)
    local_state.set_cursor(len(curr_line) - len(curr_line.lstrip()), y)


def shift_selection_right(local_state):
    """
    Implements functionality of > in vim
    by adding whitespace to beginning of each line
    TODO: Magic number whitespace, number of white space should
    be variable
    """
    px, py, pt = local_state.get_visual_anchors()
    nx, ny, nt = local_state.get_page_state()
    td = len(c_map['Tab'])

    start, end = (
        (py + pt, ny + nt), (ny + nt, py + pt))[(ny + nt) < (py + pt)]
    for n in range(start, end + 1):
        l = local_state.get_line(n)
        local_state.set_line(n, ' ' * td + l)


def shift_selection_left(local_state):
    """
    Implements functionality of < in vim
    by adding whitespace to beginning of each line
    TODO: Magic number whitespace, number of white space should
    be variable
    """
    px, py, pt = local_state.get_visual_anchors()
    nx, ny, nt = local_state.get_page_state()
    td = len(c_map['Tab'])

    start, end = (
        (py + pt, ny + nt), (ny + nt, py + pt))[(ny + nt) < (py + pt)]
    for n in range(start, end + 1):
        l = local_state.get_line(n)
        local_state.set_line(n, l[:td].strip() + l[td:])


def delete_text_char(local_state):
    """
    Delete single character in line
    Have to watch out for deleteing a
    character at the beginning of a line
    """
    x, y, curr_top = local_state.get_page_state()
    curr_line = local_state.get_line(y + curr_top)

    if x > 0:
        local_state.set_line(curr_top + y, curr_line[:x - 1] + curr_line[x:])
        local_state.set_cursor(x - 1, y)
    elif y > 0 or curr_top > 0:
        if curr_line == '\n':
            local_state.remove_line(curr_top + y)
            local_state.set_cursor(0, y - 1)
            cursor_logic.move_cursor_end_line(local_state)
        else:
            prev_line = local_state.get_line(y + curr_top - 1)
            local_state.remove_line(curr_top + y)
            local_state.set_line(
                curr_top + y - 1,
                prev_line[:-1] + curr_line
            )  # slice off new line + last character
            local_state.set_cursor(len(prev_line) - 1, y - 1)


def delete_text_range(px, py, pt, nx, ny, nt, local_state):
    """
    Delete characters within given range by first finding the
    'final' x and y location of cursor and performing delete
    in that direction.
    final cursor location should be at fx, fy
    on which of ny + nt or py + pt comes first
    """
    fx, fy = ((px, py), (nx, ny))[(ny + nt) < (py + pt)]

    if py + pt == ny + nt:
        start, end = ((px, nx), (nx, px))[nx < px]
        curr_line = local_state.get_line(py + pt)
        local_state.set_line(py + pt, curr_line[:start] + curr_line[end:])
        local_state.set_cursor(start, py)
    else:
        start, end = (
            (py + pt, ny + nt), (ny + nt, py + pt))[(ny + nt) < (py + pt)]
        count = 0
        for n in range(start, end + 1):
            if (n == py + pt) and (px, py) == (fx, fy):
                local_state.set_line(n, local_state.get_line(n)[:px] + '\n')
            elif (n == py + pt) and (px, py) != (fx, fy):
                local_state.set_line(n, local_state.get_line(n)[px:])
            elif (n == ny + nt) and (nx, ny) == (fx, fy):
                local_state.set_line(n, local_state.get_line(n)[:nx] + '\n')
            elif (n == ny + nt) and (nx, ny) != (fx, fy):
                local_state.set_line(n, local_state.get_line(n)[nx:])
            else:
                count += 1

        for i in range(count):
            local_state.remove_line(start + 1)

        local_state.set_cursor(fx, fy)


def get_text_range(px, py, pt, nx, ny, nt, local_state):
    """
    Get text in given range arguments.
    Similar to delete text in range except strings
    are appended to a list and returned
    """
    txt = []
    fx, fy = ((nx, ny), (px, py))[(ny + nt) < (py + pt)]

    if py + pt == ny + nt:
        start, end = ((px, nx), (nx, px))[nx < px]
        curr_line = local_state.get_line(py + pt)
        txt.append(curr_line[start:end + 1])
    else:
        start, end = (
            (py + pt, ny + nt), (ny + nt, py + pt))[(ny + nt) < (py + pt)]
        for n in range(start, end + 1):
            if (n == py + pt) and (px, py) == (fx, fy):
                txt.append(local_state.get_line(n)[:px])
            elif (n == py + pt) and (px, py) != (fx, fy):
                txt.append(local_state.get_line(n)[px:])
            elif (n == ny + nt) and (nx, ny) == (fx, fy):
                txt.append(local_state.get_line(n)[:nx])
            elif (n == ny + nt) and (nx, ny) != (fx, fy):
                txt.append(local_state.get_line(n)[nx:])
            else:
                txt.append(local_state.get_line(n))
    return txt


def add_new_line_char(local_state):
    """
    Split line from x based on x coordinate of cursor,
    add a new line delimiter and append the rest of the
    string to the following line
    """
    x, y, curr_top = local_state.get_page_state()
    curr_line = local_state.get_line(y + curr_top)

    local_state.set_line(
        y + curr_top,
        curr_line[:x] + '\n'  # python string splicing doesn't index exceptions
    )
    local_state.add_line(y + curr_top + 1, curr_line[x:])

    local_state.set_cursor(0, y + 1)
