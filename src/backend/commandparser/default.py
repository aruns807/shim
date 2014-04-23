import re


DEFAULT_COMMAND_TOKENS = {
    re.compile('[0-9]+'): {
        'type':'NUMBER',
        'terminal': False
    },
    re.compile('f.'): {
        'type':'FIND_CHARACTER',
        'terminal': False
    },
    re.compile('d'): {
        'type': 'DELETE_INIT',
        'terminal': False
    },
    re.compile('dd'): {
        'type': 'DELETE_LINE',
        'terminal': True
    },
    re.compile('[h|j|k|l|w|b|\{|\}]'): {
        'type': 'MOVEMENT',
        'terminal': True
    },
    re.compile('yy'): {
        'type': 'YANK_LINE',
        'terminal': True
    },
    re.compile('gg'): {
        'type': 'GO_TO_LINE_NUM',
        'terminal': True
    },
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
}
