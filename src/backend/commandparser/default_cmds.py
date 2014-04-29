import re


DEFAULT_COMMAND_TOKENS = {
    re.compile('[0-9]+'): {
        'type':'NUMBER',
    },
    re.compile('f.'): {
        'type':'FIND_CHARACTER',
    },
    re.compile('d'): {
        'type': 'DELETE_INIT',
    },
    re.compile('dd'): {
        'type': 'DELETE_LINE',
    },
    re.compile('[h|j|k|l|w|b|\{|\}]'): {
        'type': 'MOVEMENT',
    },
    re.compile('yy'): {
        'type': 'YANK_LINE',
    },
    re.compile('gg'): {
        'type': 'GO_TO_LINE_NUM',
    },
    re.compile('m[a-z]'): {
        'type': 'MARK_POSITION',
    },
    re.compile('\'[a-z]'): {
        'type': 'JUMP_MARK',
    }
}


DEFAULT_COMMAND_MAP = {
    'YANK_LINE': 'YANK_LINE',
    'FIND_CHARACTER': 'FIND_CHARACTER',
    'NUMBER|GO_TO_LINE_NUM': 'JUMP_LINE_NUM',
    'GO_TO_LINE_NUM': 'GO_FILE_BEGIN',
    'DELETE_INIT|MOVEMENT': 'DELETE_MOVEMENT',
    'DELETE_LINE': 'DELETE_LINE',
    'NUMBER|DELETE_LINE': 'DELETE_LINE_REPEAT',
    'NUMBER|MOVEMENT': 'REPEAT_MOVEMENT',
    'MARK_POSITION': 'MARK_POSITION',
    'JUMP_MARK': 'JUMP_MARK',
}
