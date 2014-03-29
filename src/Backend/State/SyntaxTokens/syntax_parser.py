# Syntax parsing module using pygments
# This module needs a lot of work
# Potentially this can be sped up even more
# if we roll our own syntax parser since
# there would be no need for parsing each line over and over
# TODO: Discuss alternatives to this module.
# TODO: Make syntax highlighter work for things that aren't python

from pygments import lex
from pygments.lexers import get_lexer_for_filename, get_lexer_by_name
from pygments.token import Token
from Backend.State.SyntaxTokens.color_config import options

class syntax_parser():

    def __init__(self, filename):
        """
        init by getting a lexer for file name
        If none exist set lexer to dummy which will be
        caught in parse
        """
        try:
            self.lexer = get_lexer_for_filename(filename)
        except:
            self.lexer = None

    def parse_string(self, s):
        """
        Parse string using lexer, if none exists
        return string with default text color
        """
        start = 0
        ret_list = []
        if self.lexer is None:
            return ([(0, s, options['text_color'])])

        for token in lex(s, self.lexer):
            color = self.determine_color(token[0])
            ret_list.append((start, token[1], color))
            start += len(token[1])
        return ret_list

    def determine_color(self, t):
        """
        This can be sped up by putting it into a preloaded dict
        """
        if t is Token.Name.Class or t is Token.Name.Function:
            return options['function_name_color']
        elif t is Token.Keyword:
            return options['keyword_color']
        elif t is Token.String or t is Token.Literal.String.Interpol:
            return options['string_color']
        elif t is Token.Comment:
            return options['comment_color']
        elif t is Token.Keyword.Namespace:
            return options['namespace_color']
        else:
            return options['text_color']
