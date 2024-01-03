from typing import NamedTuple, List, Union

class Atom(NamedTuple):
    char: str
    def __repr__(self):
        return f'{self.char}'
class Cons(NamedTuple):
    char: str
    v: List[Union['Atom', 'Cons']]
    def __repr__(self):
        return f'({self.char} ' + ' '.join([str(s) for s in self.v]) + ')'

class Lexer():
    def __init__(self, s):
        self.s = s.replace(" ", "")
        self.i = -1
    def next(self):
        self.i += 1
        return self.s[self.i]
    def peek(self):
        return self.s[self.i+1] if self.i+1 < len(self.s) else None

infix_binding_power = {
    '+': (1, 2), '-': (1, 2), 
    '*': (3, 4), '/': (3, 4),
    '.': (8, 7)
}

def parse(s):
    return pratt(Lexer(s), 0)

def pratt(lexer, min_bp) -> Union['Atom', 'Cons']:
    lhs = Atom(lexer.next())
    while True:
        if (op := lexer.peek()) is None:
            break
        l_bp, r_bp = infix_binding_power[op]
        if l_bp < min_bp:
            break
        lexer.next()
        rhs = pratt(lexer, r_bp)
        lhs = Cons(op, [lhs, rhs])
    return lhs

def tests():
    assert(str(parse("1")) == "1")
    assert(str(parse("1 + 2")) == "(+ 1 2)")
    assert(str(parse("1 + 2 * 3")) == "(+ 1 (* 2 3))")

tests()
