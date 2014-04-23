import re

EX_COMMAND_TOKENS = {
    re.compile('w'): {
        'type':'WRITE',
        'terminal': False
    },
    re.compile('q'): {
        'type':'QUIT',
        'terminal': False
    },
}


EX_COMMAND_MAP = {
    'WRITE': 'WRITE',
    'QUIT': 'QUIT',
    'WRITE|QUIT': 'WRITE_AND_QUIT',
}
