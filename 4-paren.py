from typing import Union
from cons import Atom, Cons

class Lexer():
    def __init__(self, s):
        self.s = s.replace(" ", "") # for repr
        self.toks = list(self.s[::-1])
    def consume(self):
        return self.toks.pop()
    def is_done(self):
        if self.peek() == ')':
            self.consume()
            return True
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
    '.': 1, # function composition
    '!': 1, # factorial
    '$': 0, # function application
    '|': 0, # derivative
    '(': 0, # grouping, kinda wrong way of thinking about it
}

infix_bp = {
    '+': 1, '-': 1,
    '.': 2,
    '*': 3, '/': 3,
    '^': 4,
    '$': 5,
    '|': 6,
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
    elif lexer.peek() == '(':
        lexer.consume()
        lhs = pratt(lexer, 0)
    else:
        lhs = Atom(lexer.consume())

    while not lexer.is_done():
        op = lexer.peek()
        if lexer.peek_juxtapose():
            op = {0: '*', 1: '*', 2: '|'}[order(lhs)]
        bp = infix_bp[op] + assoc[op] if op != '(' else 0

        if op == '(':
            op = {0: '*', 1: '$', 2: '|'}[order(lhs)]

        if infix_bp[op] < min_bp:
            break
        if not lexer.peek_juxtapose():
            lexer.consume()
        rhs = pratt(lexer, bp)
        lhs = Cons([Atom(op), lhs, rhs])
    return lhs

# O(height of taking lefts down tree).
# could be O(1) if we stored an `order` on 
# each sexp (the recursion would be attr lookup)
def order(exp):
    orders = {'D': 2, 
            'f': 1, 'g': 1}
    if isinstance(exp, Atom):
        return orders.get(exp.char, 0)
    if isinstance(exp.v[0], Atom):
        if exp.v[0].char == '^' and orders[exp.v[1].char] == 2:
            return 2
        else:
            return order(exp.v[-1])
    return order(exp.v[0]) - 1
