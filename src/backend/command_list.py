# Python variables containing useful mapping translations
# i.e Tkinter keysym event mapping to useful character mapping
# like 'comma': ','
# This should be able to be manipulated by the user in some fashion
# to enable custom key mappings and potentially more(design required)
# TODO: fix hard coded tab width

COMMAND_MAP = {
    'dollar': '$',
    'braceright': '}',
    'braceleft': '{',
    'bracketright': ']',
    'bracketleft': '[',
    'parenright': ')',
    'parenleft': '(',
    'colon': ':',
    'semicolon': ';',
    'bar': '|',
    'greater': '>',
    'less': '<',
    'comma': ',',
    'period': '.',
    'slash': '/',
    'question': '?',
    'plus': '+',
    'equal': '=',
    'minus': '-',
    'underscore': '_',
    'exclam': '!',
    'at': '@',
    'percent': '%',
    'asciicircum': '^',
    'ampersand': '&',
    'asterisk': '*',
    'quoteright': "'",
    'quotedbl': '"',
    'BackSpace': 'BackSpace',
    'Return': 'Return',
    'space': ' ',
    'Up': '<Up>',
    'Down': '<Down>',
    'Left': '<Left>',
    'Right': '<Right>',
    'Tab': '    ',
    '<Control-braceright>': '<Control-bracketright>',
    '<Control-braceleft>': '<Control-bracketleft>',
}


DEFAULT_MOVEMENTS = {
    'p': ['paste'],
    # 'u': ['undo_command'],
    'k': ['move_cursor_up'],
    'h': ['move_cursor_left'],
    'j': ['move_cursor_down'],
    'l': ['move_cursor_right'],
    '<Up>': ['move_cursor_up'],
    '<Left>': ['move_cursor_left'],
    '<Down>': ['move_cursor_down'],
    '<Right>': ['move_cursor_right'],
    'A': ['insert_end_of_line'],
    'G': ['move_cursor_end_file'],
    '$': ['move_cursor_end_line'],
    'O': ['insert_new_line_above'],
    'o': ['insert_new_line_below'],
    'x': ['delete_text_highlight'],
    # '<Control-r>': ['redo_command'],
    'gg': ['move_cursor_begin_file'],
    'e': ['move_cursor_next_word_end'],
    '}': ['move_cursor_next_paragraph'],
    '{': ['move_cursor_prev_paragraph'],
    '0': ['move_cursor_beginning_line'],
    'w': ['move_cursor_next_word_front'],
    'b': ['move_cursor_prev_word_front'],
    '<Control-braceright>': ['move_next_instance_buffer'],
    '<Control-braceleft>': ['move_prev_instance_buffer'],
}


DEFAULT_COMMAND_LEADERS = set(['g', 'f', 'd', 'y'])


VISUAL_MOVEMENTS = {
    'k': ['move_cursor_up'],
    'h': ['move_cursor_left'],
    'j': ['move_cursor_down'],
    'l': ['move_cursor_right'],
    '<Up>': ['move_cursor_up'],
    '<Left>': ['move_cursor_left'],
    '<Down>': ['move_cursor_down'],
    '<Right>': ['move_cursor_right'],
    '<': ['shift_selection_left'],
    'G': ['move_cursor_end_file'],
    '$': ['move_cursor_end_line'],
    '>': ['shift_selection_right'],
    'x': ['delete_text_highlight'],
    'gg': ['move_cursor_begin_file'],
    'e': ['move_cursor_next_word_end'],
    '}': ['move_cursor_next_paragraph'],
    '{': ['move_cursor_prev_paragraph'],
    '0': ['move_cursor_beginning_line'],
    'w': ['move_cursor_next_word_front'],
    'b': ['move_cursor_prev_word_front'],
}


DEFAULT_BREAK_MOVEMENTS = {
    'k': ['move_cursor_up'],
    'h': ['move_cursor_left'],
    'j': ['move_cursor_down'],
    'l': ['move_cursor_right'],
    '<Up>': ['move_cursor_up'],
    '<Left>': ['move_cursor_left'],
    '<Down>': ['move_cursor_down'],
    '<Right>': ['move_cursor_right'],
    'w': ['move_cursor_next_word_front'],
    'b': ['move_cursor_prev_word_front'],
    'x': ['delete_text_highlight'],
}


VISUAL_BREAK_MOVEMENTS = {
    'y': ['visual_yank']
}
