编写一个简单的Lexer与Parser.md
================================================================================

__测试版本__：Python3.10.8

--------------------------------------------------------------------------------

Python标准库的 `re` 模块合理利用可以大幅度简化词法分析器和语法分析器的编写。

```python
import re
from enum import auto
from enum import Enum
from operator import add, sub, mul, truediv
from collections import OrderedDict
from collections import namedtuple

class Token:

    class Type(Enum):
        NUM        = auto()
        ADD        = auto()
        SUB        = auto()
        MUL        = auto()
        DIV        = auto()
        LPAREN     = auto()
        RPAREN     = auto()
        EOL        = auto()
        WHITESPACE = auto()
        ILLEGAL    = auto()

    def __init__(self, ttype, tvalue):
        self.ttype = ttype
        self.tvalue = tvalue

    def __repr__(self):
        return f'Token {self.ttype:<24} {self.tvalue or ""}'

class Lexer:

    def __init__(self):
        self.tokens = list()
        self.modes = OrderedDict()
        self.add_mode(Token.Type.NUM,        lambda ttype, ttext: Token(ttype, float(ttext)), r'\d+(\.\d+)?')
        self.add_mode(Token.Type.ADD,        lambda ttype, ttext: Token(ttype, add),          r'\+')
        self.add_mode(Token.Type.SUB,        lambda ttype, ttext: Token(ttype, sub),          r'\-')
        self.add_mode(Token.Type.MUL,        lambda ttype, ttext: Token(ttype, mul),          r'\*')
        self.add_mode(Token.Type.DIV,        lambda ttype, ttext: Token(ttype, truediv),      r'\/')
        self.add_mode(Token.Type.LPAREN,     lambda ttype, ttext: Token(ttype, None),         r'\(')
        self.add_mode(Token.Type.RPAREN,     lambda ttype, ttext: Token(ttype, None),         r'\)')
        self.add_mode(Token.Type.EOL,        lambda ttype, ttext: Token(ttype, None),         r'\n')
        self.add_mode(Token.Type.WHITESPACE, lambda ttype, ttext: None,                       r'[ \t]')
        self.add_mode(Token.Type.ILLEGAL,    lambda ttype, ttext: None,                       r'.')

    def add_mode(self, ttype, func, regexp):
        modeinfo = namedtuple("modeinfo", "func regexp")
        mi = modeinfo(func, f'(?P<{ttype.name}>{regexp})')
        self.modes[ttype] = mi

    def lex(self, code):
        self.tokens.clear()
        fullregexp = "|".join(tuple(map(lambda item: item.regexp, self.modes.values())))
        fullpat = re.compile(fullregexp)
        scanner = fullpat.scanner(code)
        for m in iter(scanner.match, None):
            sttype, ttext = m.lastgroup, m.group()
            ttype = Token.Type[sttype]
            if ttype == Token.Type.ILLEGAL:
                raise SyntaxError(f"Illegal character '{tokentext}'\n")
            mode = self.modes[ttype]
            func = mode.func
            tok = func(ttype, ttext)
            if tok:
                self.tokens.append(tok)

class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.cursor = -1

    def advance(self, n=1):
        self.cursor += n

    def accept(self, *ttypes):
        for idx, ttype in enumerate(ttypes, 1):
            tok = self.next_token(idx)
            if (not tok) or (tok.ttype != ttype):
                return False
        self.advance(len(ttypes))
        return True

    def current_token(self):
        return self.lexer.tokens[self.cursor]

    def next_token(self, idx=1):
        targetidx = self.cursor + idx
        if len(self.lexer.tokens) < targetidx + 1:
            return None
        return self.lexer.tokens[targetidx]

    def parse(self, code):
        self.cursor = -1
        self.lexer.lex(code)
        return self.expr()

    def expr(self):
        """
        expr = term ADD term
             | term SUB term
             | term
             ;
        """
        val = self.term()
        while self.accept(Token.Type.ADD) or self.accept(Token.Type.SUB):
            op = self.current_token().tvalue
            rv = self.term()
            val = op(val, rv)
        return val

    def term(self):
        """
        expr = factor MUL factor
             | factor DIV factor
             | factor
             ;
        """
        val = self.factor()
        while self.accept(Token.Type.MUL) or self.accept(Token.Type.DIV):
            op = self.current_token().tvalue
            rv = self.factor()
            val = op(val, rv)
        return val

    def factor(self):
        """
        expr = NUM
             | LPAREN expr RPAREN
             ;
        """
        if self.accept(Token.Type.NUM):
            tok = self.current_token()
            return tok.tvalue
        elif self.accept(Token.Type.LPAREN):
            val = self.expr()
            if not self.accept(Token.Type.RPAREN):
                raise SyntaxError("Expected closing parenthese")
            return val
        raise SyntaxError("Expected number")

lexer = Lexer()
parser = Parser(lexer)
print(parser.parse("(4 + 2 * (3 + 4)) / 3.14"))
```
