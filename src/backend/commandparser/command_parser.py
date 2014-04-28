# logic for parsing command buffer string and determining commands
# interfaces with shim through the in the parse_buffer function
# TODO: currently parser does a greedy scan of possible tokens
# per iteration and selects longest token, this might not actually work.
# TODO: RENAME THIS FILE COMMAND PARSER IS FULLY OBSOLETE
import re
from copy import deepcopy
from backend import command_list
from backend.commandparser.default_cmds import DEFAULT_COMMAND_TOKENS, DEFAULT_COMMAND_MAP
from backend.commandparser.ex_cmds import EX_COMMAND_TOKENS, EX_COMMAND_MAP

# BEGIN YANKED FUNCTIONS, TODO: CLEAN THIS UP
def goto_line_num(s):
    ind = s.find('gg')
    if ind == 0:
        return ['move_cursor_begin_file']
    else:
        count = 'n' + s[:ind]
        return [count, 'move_cursor_line_num']


def go_file_begin(s):
    return ['move_cursor_begin_file']


def seek_char(s):
    # assumption is that the regex will only return a string of length 2,
    # seems kind of reasonable
    return ['c' + s[1], 'move_cursor_seek_char']


def repeat_default_movement(s):
    n_arg = re.search('[0-9]*', s).group()
    return ['r' + n_arg, command_list.DEFAULT_MOVEMENTS[s[len(n_arg):]][0]]


def delete_text_movement(s):
    return ['s' + command_list.DEFAULT_MOVEMENTS[s[1:]][0],
            'delete_text_movement']


def delete_curr_line(s):
    n_arg = re.search('[0-9]*', s).group()
    if bool(n_arg):
        return ['r' + n_arg, 'delete_curr_line']
    else:
        return ['delete_curr_line']


def yank_curr_line(s):
    return ['yank_curr_line']


def quit(s):
    return ['quit']


def write(s):
    return ['write']

def write_and_quit(s):
    return ['write_and_quit']
# END YANKED FUNCTIONS, TODO: CLEAN THIS UP

def mark_position(s):
    buf = s[-1]
    return ['c' + buf, 'mark_location']


COMMAND_MAP = {
    'JUMP_LINE_NUM': goto_line_num,
    'FIND_CHARACTER': seek_char,
    'REPEAT_MOVEMENT': repeat_default_movement,
    'DELETE_MOVEMENT': delete_text_movement,
    'DELETE_LINE': delete_curr_line,
    'YANK_LINE': yank_curr_line,
    'GO_FILE_BEGIN': go_file_begin,
    'WRITE': write,
    'QUIT': quit,
    'WRITE_AND_QUIT': write_and_quit,
    'MARK_POSITION': mark_position
}


class token():

    def __init__(self, t, r):
        self.type = t
        self.raw = r

    def __repr__(self):
        return 'type: %s | raw: %s' % (self.type, self.raw)

    def get_token(self):
        return self.type, self.val

    def get_type(self):
        return self.type


class parser():

    def __init__(self, mode):
        mode_dct ={
            'default': {
                'tokens': DEFAULT_COMMAND_TOKENS,
                'cmds': DEFAULT_COMMAND_MAP,
            },
            'ex': {
                'tokens': EX_COMMAND_TOKENS,
                'cmds': EX_COMMAND_MAP,
            },
        }
        self._tokens = mode_dct[mode]['tokens']
        self._cmds = mode_dct[mode]['cmds']

    def try_tok_str(self, s):
        matches = []
        for regex, res in self._tokens.items():
            result = regex.match(s)
            if bool(result):
                matches.append((result.group(), res))

        if not len(matches):
            return False
        return max(matches, key=lambda t: t[0])

    def try_cmd_match(self, res):
        res = [tok.get_type() for tok in res]
        for pattern, cmd in self._cmds.items():
            if res == pattern.split('|'):
                return cmd
        return None

    def parse_string(self, s):
        result = []
        has_match = True
        os, cs = deepcopy(s), deepcopy(s)
        while has_match:
            match = self.try_tok_str(cs)
            result.append(
                token(match[1]['type'], match[0])
            )
            cs = cs[len(match[0]):]
            has_match = self.try_tok_str(cs)
        cmd = self.try_cmd_match(result)
        if cmd != None:
            return COMMAND_MAP[cmd](os)
        else:
            return ''
