# All local file state is saved in an instance class
# Multiple files being open at the same time would correspond to
# multiple instance classes being open at the same time

import os
from copy import deepcopy
from backend.state.syntaxtokens import syntax_parser

class instance():

    def __init__(self, filename):
        self._filename = filename
        self._parser = syntax_parser.syntax_parser(filename)
        if os.path.exists(filename):
            self._lines = [
                line for line in open(filename, 'r')
            ]
            self._line_tokens = [
                self._parser.parse_string(line) for line in open(filename, 'r')
            ]
        else:
            self._lines = ['']
            self._line_tokens = ['']

        self._cursor_x, self._cursor_y, self._curr_top = 0, 0, 0
        self._visual_x, self._visual_y, self._visual_curr_top = 0, 0, 0
        self._undo_buffer, self._undo_index = [], -1
        self._marks = {}

    def check_repeat_additions(self, diff, last_state):
        return (
            diff[0] == '+' and last_state[0] == '+'
            and diff[1] == last_state[2]['last_addition'] + 1
        )

    def check_repeat_deletions(self, diff, last_state):
        return (
            diff[0] == '-' and last_state[0] == '-'
            and diff[1] == last_state[1]
        )

    def check_repeat_modifications(self, diff, last_state):
        return (
            diff[0] == 'm' and last_state[0] == 'm'
            and diff[1] == last_state[1]
        )

    def add_to_undo_buffer(self, diff):
        """
        Only add to undo buffer is move is not to be coalesced into
        previous undo block
        """
        if self._undo_index == len(self._undo_buffer) - 1:
            try:
                last_state = self._undo_buffer[self._undo_index]
            except IndexError:
                self._undo_buffer.append(diff)
                self._undo_index += 1
                return

            # repeat addtions to the same line
            if self.check_repeat_additions(diff, last_state):
                last_state[2]['count'] += 1
                last_state[2]['last_addition'] += 1
            # repeat deletions from the same line
            elif self.check_repeat_deletions(diff, last_state):
                last_state[2]['lines'].append(diff[2]['lines'][0])
                last_state[2]['line_tokens'].append(diff[2]['line_tokens'][0])
            # repeat modifications to the same line
            elif self.check_repeat_modifications(diff, last_state):
                last_state[2]['new']['line'] = \
                    diff[2]['new']['line']
                last_state[2]['new']['line_token'] = \
                    diff[2]['new']['line_token']
            else:
                self._undo_buffer.append(diff)
                self._undo_index += 1
                if len(self._undo_buffer) > 100:
                    self._undo_buffer.pop(0)
        else:
            self._undo_buffer = (
                self._undo_buffer[:self._undo_index] + [diff], [diff]
            )[self._undo_index == -1]
            self._undo_index += 1

    def undo_line_modification(self, diff):
        self._lines[diff[1]] = diff[2]['old']['line'][0]
        self._line_tokens[diff[1]] = diff[2]['old']['line_token'][0]

    def undo_line_addition(self, diff):
        for i in range(diff[2]['count']):
            self._lines.pop(diff[1])
            self._line_tokens.pop(diff[1])

    def undo_line_removal(self, diff):
        for i in range(len(diff[2]['lines'])):
            self._lines.insert(i + diff[1], diff[2]['lines'][i])
            self._line_tokens.insert(i + diff[1], diff[2]['line_tokens'][i])

    def undo_state(self):
        """
        Only undo if there is an action to undo
        set cursor and curr_top coordinates to saved coordinates
        """
        if self._undo_index != -1:
            # diff = self._undo_buffer.pop(-1)
            diff = self._undo_buffer[self._undo_index]
            self._undo_index -= 1
            if diff[0] == 'm':
                self.undo_line_modification(diff)
            elif diff[0] == '+':
                self.undo_line_addition(diff)
            elif diff[0] == '-':
                self.undo_line_removal(diff)

            (x, y, z) = diff[2]['state']
            self.set_curr_top(z)
            self.set_cursor(x, y)

    def redo_line_modification(self, diff):
        self._lines[diff[1]] = diff[2]['new']['line'][0]
        self._line_tokens[diff[1]] = diff[2]['new']['line_token'][0]

    def redo_line_addition(self, diff):
        for i in range(diff[2]['count']):
            self._lines.insert(diff[1] + i, diff[2]['data']['lines'][i])
            self._line_tokens.insert(
                diff[1] + i, diff[2]['data']['line_tokens'][i]
            )

    def redo_line_removal(self, diff):
        for i in range(len(diff[2]['lines'])):
            self._lines.pop(diff[1])
            self._line_tokens.pop(diff[1])

    def redo_state(self):
        """
        Only redo if there is an action to redo
        """
        if self._undo_index < len(self._undo_buffer) - 1:
            self._undo_index += 1
            diff = self._undo_buffer[self._undo_index]
            if diff[0] == 'm':
                self.redo_line_modification(diff)
            if diff[0] == '+':
                self.redo_line_addition(diff)
            if diff[0] == '-':
                self.redo_line_removal(diff)

    def get_line(self, index):
        return self._lines[index]

    # line numbers are 0 indexed
    def get_lines(self):
        return self._lines

    def get_line_tokens(self):
        return self._line_tokens

    def get_cursor(self):
        return self._cursor_x, self._cursor_y

    def get_curr_top(self):
        return self._curr_top

    def get_line_height(self):
        return self._line_height

    def get_line_num(self):
        return len(self._lines)

    def get_filename(self):
        return self._filename

    def get_page_state(self):
        return self._cursor_x, self._cursor_y, self._curr_top

    def get_visual_anchors(self):
        return self._visual_x, self._visual_y, self._visual_curr_top

    def set_mark(self, buf, loc):
        self._marks[buf] = loc

    def add_line(self, index, line):
        """
        Save lines added in memory so undo and
        redo can be performed
        """
        try:
            li = self._lines[index]
            lt = self._line_tokens[index]
        except IndexError:
            li = ''
            lt = self._parser.parse_string('')

        d = {
            'count': 1,
            'data': {
                'lines': [li],
                'line_tokens': [lt],
            },
            'state': self.get_page_state(),
            'last_addition': index,
        }

        # self.add_to_undo_buffer(('+', index, d))
        self._lines.insert(index, line)
        self._line_tokens.insert(index, self._parser.parse_string(line))

    def remove_line(self, index):
        """
        Save lines removed in memory so undo and
        redo can be performed
        """
        d = {
            'lines': [self._lines[index]],
            'line_tokens': [self._line_tokens[index]],
            'state': self.get_page_state(),
        }
        # self.add_to_undo_buffer(('-', index, d))
        self._lines.pop(index)
        self._line_tokens.pop(index)

    def set_curr_top(self, num):
        self._curr_top = num

    def set_line_height(self, num):
        self._line_height = num

    def set_line(self, ind, s):
        """
        Create dict of diff data and add it to
        undo buffer. Pick string depending upon
        undo or redo action
        """
        parsed = self._parser.parse_string(s)
        d = {
            'old': {
                'line': [self._lines[ind]],
                'line_token': [self._line_tokens[ind]]
            },
            'new': {
                'line': [s],
                'line_token': [parsed],
            },
            'state': self.get_page_state()
        }

        # self.add_to_undo_buffer(('m', ind, d))
        self._lines[ind] = s
        self._line_tokens[ind] = parsed

    def set_visual_anchor(self, x=None, y=None, curr_top=None):
        """
        Set anchors to cursor and curr_top values if no
        arguments ar passed in
        """
        self._visual_x = x if x is not None else self._cursor_x
        self._visual_y = y if y is not None else self._cursor_y
        self._visual_curr_top = \
            curr_top if curr_top is not None else self._curr_top

    def set_cursor(self, x, y):
        """
        Set cursor while making sure cursor x and cursor y
        never get invalid values
        """
        self._cursor_x = max(x, 0)
        if y > self._line_height:
            self._curr_top += (y - self._line_height)
            self._cursor_y = self._line_height
        elif y < 0:
            self._curr_top = max(self._curr_top + y, 0)
            self._cursor_y = 0
        else:
            self._cursor_y = y
