import re

EX_COMMAND_TOKENS = {
    re.compile('w'): {
        'type':'WRITE',
    },
    re.compile('q'): {
        'type':'QUIT',
    },
}


EX_COMMAND_MAP = {
    'WRITE': 'WRITE',
    'QUIT': 'QUIT',
    'WRITE|QUIT': 'WRITE_AND_QUIT',
}
