from typing import NamedTuple, List, Union

class Atom(NamedTuple):
    char: str
    def __repr__(self):
        return f'{self.char}'
class Cons(NamedTuple):
    v: List[Union['Atom', 'Cons']]
    def __repr__(self):
        return f'(' + ' '.join([str(s) for s in self.v]) + ')'

class Lexer():
    def __init__(self, s):
        self.s = s.replace(" ", "") # for repr
        self.toks = list(self.s[::-1])
    def consume(self):
        return self.toks.pop()
    def is_done(self):
        return self.peek() is None
    def peek_juxtapose(self):
        return self.peek() not in infix_bp and self.peek() != '('
    def peek(self):
        try: return self.toks[-1]
        except IndexError: return None
    def __repr__(self):
        used = len(self.s) - len(self.toks)
        return self.s[:used] + '|' + ''.join(reversed(self.toks))

assoc = { # 1 means left-assoc: (1 - 2) - 3
    '+': 1, '-': 1, '*': 1, '/': 1,
    '^': 0,
}

infix_bp = {
    '+': 1, '-': 1, 
    '*': 2, '/': 2,
    '^': 3,
}

prefix_bp = {
    '-': 1, '+': 1,
}

def parse(s):
    return pratt(Lexer(s), 0)

def pratt(lexer, min_bp) -> Union['Atom', 'Cons']:
    if lexer.peek() in prefix_bp:
        op = lexer.consume()
        rhs = pratt(lexer, prefix_bp[op] + assoc[op])
        lhs = Cons([Atom(op), rhs])
    else:
        lhs = Atom(lexer.consume())

    while not lexer.is_done():
        op = lexer.peek()
        if lexer.peek_juxtapose():
            op = '*'
        bp = infix_bp[op] + assoc[op]

        if infix_bp[op] < min_bp:
            break
        if not lexer.peek_juxtapose():
            lexer.consume()
        rhs = pratt(lexer, bp)
        lhs = Cons([Atom(op), lhs, rhs])
    return lhs

