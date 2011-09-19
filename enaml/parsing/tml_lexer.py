#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import re
import tokenize

import ply.lex as lex


def _raise_error(message, t, klass):
    raise klass(message + ' - lineno: %s' % t.lineno)


def raise_syntax_error(message, t):
    _raise_error(message, t, SyntaxError)


def raise_indentation_error(message, t):
    _raise_error(message, t, IndentationError)


class TraitsMLLexer(object):

    #--------------------------------------------------------------------------
    # Token Declarations
    #--------------------------------------------------------------------------
    tokens = (
        'AMPER',
        'AT',
        'DOT',
        'CIRCUMFLEX',
        'COLON',
        'COMMA',
        'DEDENT',
        'DOUBLESLASH',
        'DOUBLESTAR',
        'ENDMARKER',
        'EQEQUAL', 
        'EQUAL',
        'GREATER',
        'GREATEREQUAL',
        'INDENT',
        'LBRACE',
        'LEFTSHIFT',
        'LESS',
        'LESSEQUAL',
        'LPAR',
        'LSQB',
        'MINUS',
        'NAME',
        'NEWLINE',
        'NOTEQUAL',
        'NUMBER',
        'PERCENT',
        'PLUS',
        'RBRACE',
        'RIGHTSHIFT',
        'RPAR',
        'RSQB',
        'SLASH',
        'STAR',
        'STRING',
        'TILDE',
        'VBAR',
        'WS',

        # string token sentinels
        'STRING_START_SINGLE',
        'STRING_START_TRIPLE',
        'STRING_CONTINUE',
        'STRING_END',

        # TML Specific Tokens
        'COLONEQUAL',

    )

    reserved = {
        'and': 'AND',
        'as': 'AS',
        'else': 'ELSE',
        'from': 'FROM',
        'for': 'FOR',
        'if': 'IF',
        'import': 'IMPORT',
        'in': 'IN',
        'is': 'IS',
        'lambda': 'LAMBDA',
        'not': 'NOT',
        'or': 'OR',
        'pass': 'PASS'
    }

    tokens = tokens + tuple(reserved.values())

    #--------------------------------------------------------------------------
    # Lexer States
    #--------------------------------------------------------------------------
    states = (
        ('SINGLEQ1', 'exclusive'),
        ('SINGLEQ2', 'exclusive'),
        ('TRIPLEQ1', 'exclusive'),
        ('TRIPLEQ2', 'exclusive'),
    )

    #--------------------------------------------------------------------------
    # INITIAL State Rules
    #--------------------------------------------------------------------------
    t_AMPER = r'&'
    t_AT = r'@'
    t_DOT = r'\.'
    t_CIRCUMFLEX = r'\^'
    t_COLON = r':'
    t_COLONEQUAL = r':='
    t_COMMA = r','
    t_DOUBLESLASH = r'//'
    t_DOUBLESTAR = r'\*\*'
    t_EQEQUAL = r'==' 
    t_EQUAL = r'='
    t_GREATER = r'>'
    t_GREATEREQUAL = r'>='
    t_LEFTSHIFT = r'<<'
    t_LESS = r'<'
    t_LESSEQUAL = r'<='
    t_MINUS = r'-'
    t_NOTEQUAL = r'!='
    t_NUMBER = tokenize.Number
    t_PERCENT = r'\%'
    t_PLUS = r'\+'
    t_RIGHTSHIFT = r'>>'
    t_SLASH = r'/'
    t_STAR = r'\*'
    t_TILDE = r'~'
    t_VBAR = r'\|'
    
    #t_DELEGATE = r'@'

    def t_comment(self, t):
        r'[ ]*\#[^\r\n]*'
        pass
   
    def t_WS(self, t):
        r' [ \t\f]+ '
        value = t.value

        # A formfeed character may be present at the start of the
        # line; it will be ignored for the indentation calculations
        # above. Formfeed characters occurring elsewhere in the
        # leading whitespace have an undefined effect (for instance,
        # they may reset the space count to zero). 
        value = value.rsplit("\f", 1)[-1]

        # First, tabs are replaced (from left to right) by one to eight
        # spaces such that the total number of characters up to and
        # including the replacement is a multiple of eight (this is
        # intended to be the same rule as used by Unix). The total number
        # of spaces preceding the first non-blank character then
        # determines the line's indentation. Indentation cannot be split
        # over multiple physical lines using backslashes; the whitespace
        # up to the first backslash determines the indentation.
        pos = 0
        while True:
            pos = value.find("\t")
            if pos == -1:
                break
            n = 8 - (pos % 8)
            value = value[:pos] + " " * n + value[pos+1:]

        if self.at_line_start and self.paren_count == 0:
            return t

    # string continuation - ignored beyond the tokenizer level
    def t_escaped_newline(self, t):
        r"\\\n"
        t.type = "STRING_CONTINUE"
        # Raw strings don't escape the newline
        assert not self.is_raw, "only occurs outside of quoted strings"
        t.lexer.lineno += 1

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.type = 'NEWLINE'
        if self.paren_count == 0:
            return t
    
    def t_LPAR(self, t):
        r'\('
        self.paren_count += 1
        return t

    def t_RPAR(self, t):
        r'\)'
        self.paren_count -= 1
        return t
    
    def t_LBRACE(self, t):
        r'\{'
        self.paren_count += 1
        return t

    def t_RBRACE(self, t):
        r'\}'
        self.paren_count -= 1
        return t
    
    def t_LSQB(self, t):
        r'\['
        self.paren_count += 1
        return t

    def t_RSQB(self, t):
        r'\]'
        self.paren_count -= 1
        return t

    #--------------------------------------------------------------------------
    # State string escapes
    #--------------------------------------------------------------------------
    def t_SINGLEQ1_SINGLEQ2_TRIPLEQ1_TRIPLEQ2_escaped(self, t):
        r"\\(.|\n)"
        t.type = "STRING_CONTINUE"
        t.lexer.lineno += t.value.count("\n")
        return t

    #--------------------------------------------------------------------------
    # TRIPLEQ1 strings
    #--------------------------------------------------------------------------
    def t_start_triple_quoted_q1_string(self, t):
        r"[uU]?[rR]?'''"
        t.lexer.push_state("TRIPLEQ1")
        t.type = "STRING_START_TRIPLE"
        if "r" in t.value or "R" in t.value:
            self.is_raw = True
        t.value = t.value.split("'", 1)[0]
        return t
    
    def t_TRIPLEQ1_simple(self, t):
        r"[^'\\]+"
        t.type = "STRING_CONTINUE"
        t.lexer.lineno += t.value.count("\n")
        return t

    def t_TRIPLEQ1_q1_but_not_triple(self, t):
        r"'(?!'')"
        t.type = "STRING_CONTINUE"
        return t

    def t_TRIPLEQ1_end(self, t):
        r"'''"
        t.type = "STRING_END"
        t.lexer.pop_state()
        self.is_raw = False
        return t
    
    # supress PLY warning
    t_TRIPLEQ1_ignore = ''

    def t_TRIPLEQ1_error(self, t):
        raise_syntax_error('Invalid Syntax', t)

    #--------------------------------------------------------------------------
    # TRIPLEQ2 strings
    #--------------------------------------------------------------------------
    def t_start_triple_quoted_q2_string(self, t):
        r'[uU]?[rR]?"""'
        t.lexer.push_state("TRIPLEQ2")
        t.type = "STRING_START_TRIPLE"
        if "r" in t.value or "R" in t.value:
            self.is_raw = True
        t.value = t.value.split('"', 1)[0]
        return t

    def t_TRIPLEQ2_simple(self, t):
        r'[^"\\]+'
        t.type = "STRING_CONTINUE"
        t.lexer.lineno += t.value.count("\n")
        return t

    def t_TRIPLEQ2_q2_but_not_triple(self, t):
        r'"(?!"")'
        t.type = "STRING_CONTINUE"
        return t

    def t_TRIPLEQ2_end(self, t):
        r'"""'
        t.type = "STRING_END"
        t.lexer.pop_state()
        self.is_raw = False
        return t

    # supress PLY warning
    t_TRIPLEQ2_ignore = ''

    def t_TRIPLEQ2_error(self, t):
        raise_syntax_error('Invalid Syntax', t)

    #--------------------------------------------------------------------------
    # SINGLEQ1 strings
    #--------------------------------------------------------------------------
    def t_start_single_quoted_q1_string(self, t):
        r"[uU]?[rR]?'"
        t.lexer.push_state("SINGLEQ1")
        t.type = "STRING_START_SINGLE"
        if "r" in t.value or "R" in t.value:
            self.is_raw = True
        t.value = t.value.split("'", 1)[0]
        return t

    def t_SINGLEQ1_simple(self, t):
        r"[^'\\\n]+"
        t.type = "STRING_CONTINUE"
        return t

    def t_SINGLEQ1_end(self, t):
        r"'"
        t.type = "STRING_END"
        t.lexer.pop_state()
        self.is_raw = False
        return t
    
    # supress PLY warning
    t_SINGLEQ1_ignore = ''
    
    def t_SINGLEQ1_error(self, t):
        raise_syntax_error('EOL while scanning single quoted string.', t)

    #--------------------------------------------------------------------------
    # SINGLEQ2 strings
    #--------------------------------------------------------------------------
    def t_start_single_quoted_q2_string(self, t):
        r'[uU]?[rR]?"'
        t.lexer.push_state("SINGLEQ2")
        t.type = "STRING_START_SINGLE"
        if "r" in t.value or "R" in t.value:
            self.is_raw = True
        t.value = t.value.split('"', 1)[0]
        return t

    def t_SINGLEQ2_simple(self, t):
        r'[^"\\\n]+'
        t.type = "STRING_CONTINUE"
        return t

    def t_SINGLEQ2_end(self, t):
        r'"'
        t.type = "STRING_END"
        t.lexer.pop_state()
        self.is_raw = False
        return t
    
    # supress PLY warning
    t_SINGLEQ2_ignore = ''
    
    def t_SINGLEQ2_error(self, t):
        raise_syntax_error('EOL while scanning single quoted string.', t)
    
    #--------------------------------------------------------------------------
    # Miscellaneous Token Rules
    #--------------------------------------------------------------------------
    # This is placed after the string rules so r"" is not matched as a name.
    def t_NAME(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, "NAME")
        return t
    
    def t_error(self, t):
        raise_syntax_error('Invalid Syntax', t)
        
    #--------------------------------------------------------------------------
    # Normal Class Items
    #--------------------------------------------------------------------------
    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.token_stream = None
        
    def input(self, txt):
        self.lexer.input(txt)
        self.token_stream = self.make_token_stream()

        # State initialization
        self.paren_count = 0
        self.is_raw = False
        self.at_line_start = False

    def token(self):
        try:
            tok = self.token_stream.next()
            return tok
        except StopIteration:
            pass
    
    def __iter__(self):
        return self.token_stream
   
    def dedent(self, lineno):
        # Synthesize a DEDENT Token
        tok = lex.LexToken()
        tok.type = 'DEDENT'
        tok.value = None
        tok.lineno = lineno
        tok.lexpos = -1
        return tok

    def indent(self, lineno):
        # Synthesize an INDENT Token.
        tok = lex.LexToken()
        tok.type = 'INDENT'
        tok.value = None
        tok.lineno = lineno
        tok.lexpos = -1
        return tok

    def make_token_stream(self):
        token_stream = iter(self.lexer.token, None)
        token_stream = self.create_strings(token_stream)
        token_stream = self.annotate_indentation_state(token_stream)
        token_stream = self.synthesize_indentation_tokens(token_stream)
        token_stream = self.add_endmarker(token_stream)
        return token_stream

    def create_strings(self, token_stream):
        for tok in token_stream:
            if not tok.type.startswith("STRING_START_"):
                yield tok
                continue

            # This is a string start; process until string end
            start_tok = tok
            string_toks = []
            for tok in token_stream:
                if tok.type == "STRING_END":
                    break
                else:
                    assert tok.type == "STRING_CONTINUE", tok.type
                    string_toks.append(tok)
            else:
                # Reached end of input without string termination
                msg = 'EOF while scanning %s-quoted string.'
                if start_tok.type == 'STRING_START_TRIPLE':
                    msg = msg % 'triple'
                else:
                    msg = msg % 'single'
                raise_syntax_error(msg, start_tok)

            # Parse the quoted string.
            #
            # The four combinations are:
            #  "ur"  - raw_unicode_escape
            #  "u"   - unicode_escape
            #  "r"   - no need to do anything
            #  ""    - string_escape
            s = "".join(tok.value for tok in string_toks)
            quote_type = start_tok.value.lower()
            if quote_type == "":
                s = s.decode("string_escape")
            elif quote_type == "u":
                s = s.decode("unicode_escape")
            elif quote_type == "ur":
                s = s.decode("raw_unicode_escape")
            elif quote_type == "r":
                s = s
            else:
                msg = 'Unknown string quote type: %r' % quote_type
                raise AssertionError(msg)

            start_tok.type = "STRING"
            start_tok.value = s

            yield start_tok

    # Keep track of indentation state
    #
    # I implemented INDENT / DEDENT generation as a post-processing filter
    #
    # The original lex token stream contains WS and NEWLINE characters.
    # WS will only occur before any other tokens on a line.
    #
    # I have three filters.  One tags tokens by adding two attributes.
    # "must_indent" is True if the token must be indented from the
    # previous code.  The other is "at_line_start" which is True for WS
    # and the first non-WS/non-NEWLINE on a line.  It flags the check to
    # see if the new line has changed indication level.
    #
    # Python's syntax has three INDENT states
    #  0) no colon hence no need to indent
    #  1) "if 1: go()" - simple statements have a COLON but no need for an indent
    #  2) "if 1:\n  go()" - complex statements have a COLON NEWLINE and must indent
    # 
    # We only care about whitespace at the start of a line
    def annotate_indentation_state(self, token_stream):
        NO_INDENT = 0
        MAY_INDENT = 1
        MUST_INDENT = 2
        
        self.at_line_start = at_line_start = True
        indent = NO_INDENT
        saw_colon = False
        
        for token in token_stream:
            token.at_line_start = at_line_start

            if token.type == "COLON":
                at_line_start = False
                indent = MAY_INDENT
                token.must_indent = False
                
            elif token.type == "NEWLINE":
                at_line_start = True
                if indent == MAY_INDENT:
                    indent = MUST_INDENT
                token.must_indent = False

            elif token.type == "WS":
                assert token.at_line_start == True
                at_line_start = True
                token.must_indent = False

            else:
                # A real token; only indent after COLON NEWLINE
                if indent == MUST_INDENT:
                    token.must_indent = True
                else:
                    token.must_indent = False
                at_line_start = False
                indent = NO_INDENT

            yield token
            self.at_line_start = at_line_start

    def synthesize_indentation_tokens(self, token_stream):
        # A stack of indentation levels; will never pop item 0
        levels = [0]
        depth = 0
        prev_was_ws = False

        for token in token_stream:
                    
            # WS only occurs at the start of the line
            # There may be WS followed by NEWLINE so
            # only track the depth here.  Don't indent/dedent
            # until there's something real.
            if token.type == 'WS':
                assert depth == 0
                depth = len(token.value)
                prev_was_ws = True
                # WS tokens are never passed to the parser
                continue

            if token.type == 'NEWLINE':
                depth = 0
                if prev_was_ws or token.at_line_start:
                    # ignore blank lines
                    continue
                # pass the other cases on through
                yield token
                continue

            # then it must be a real token (not WS, not NEWLINE)
            # which can affect the indentation level
            prev_was_ws = False
            
            if token.must_indent:
                # The current depth must be larger than the previous level
                if not (depth > levels[-1]):
                    msg = 'Expected an indented block.'
                    raise_indentation_error(msg, token)
                levels.append(depth)
                yield self.indent(token.lineno)

            elif token.at_line_start:
                # Must be on the same level or one of the previous levels
                if depth == levels[-1]:
                    # At the same level
                    pass
                elif depth > levels[-1]:
                    # indentation increase but not in new block
                    raise_indentation_error('Unexpected indent.', token)
                else:
                    # Back up; but only if it matches a previous level
                    try:
                        i = levels.index(depth)
                    except ValueError:
                        msg = ('Unindent does not match any outer level '
                               'of indentation.')
                        raise_indentation_error(msg, token)
                    for _ in range(i + 1, len(levels)):
                        yield self.dedent(token.lineno)
                        levels.pop()

            yield token

        # Sythesize a final newline token in case the user's
        # forgot to end with a newline.
        if token.type != 'NEWLINE':
            nl = lex.LexToken()
            nl.type = 'NEWLINE'
            nl.value = None
            nl.lineno = -1
            nl.lexpos = -1
            yield nl
        
        # Must dedent any remaining levels
        if len(levels) > 1:
            assert token is not None
            for _ in range(1, len(levels)):
                yield self.dedent(token.lineno)
        
    def add_endmarker(self, token_stream):
        for tok in token_stream:
            yield tok

        end_marker = lex.LexToken()
        end_marker.type = 'ENDMARKER'
        end_marker.value = None
        end_marker.lineno = -1
        end_marker.lexpos = -1
        yield end_marker


