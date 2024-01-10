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
    def push(self, op):
        self.toks.append(op)
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
    def __repr__(self): # incorrect if you push stuff: "H|ello" -> "|*ello"
        used = len(self.s) - len(self.toks)
        return self.s[:used] + '|' + ''.join(reversed(self.toks))

assoc = { # 1 means left-assoc: (1 - 2) - 3
    '+': 1, '-': 1, '*': 1, '/': 1,
    '^': 0,
    '!': 1, # factorial
    '$': 0, # function application
    '|': 0, # operator application
    '(': 0, # grouping, kinda wrong way of thinking about it
}

infix_bp = {
    '+': 1, '-': 1, 
    '*': 2, '/': 2,
    '^': 3,
    '$': 4,
    '|': 5,
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
        bp = infix_bp.get(op,0) + assoc.get(op,0)

        if op == '(':
            op = {0: '*', 1: '$', 2: '|'}[order(lhs)]
            bp = 0
        elif op not in infix_bp:
            op = {0: '*', 1: '*', 2: '|'}[order(lhs)]
            bp = infix_bp[op] + assoc[op]

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
def order(sexp):
    orders = {'D': 2, 
            'f': 1, 'g': 1}
    if isinstance(sexp, Atom):
        return orders.get(sexp.char, 0)
    if isinstance(sexp.v[0], Atom):
        if sexp.v[0].char == '^' and orders[sexp.v[1].char] == 2:
            return 2
        else:
            return order(sexp.v[-1])
    return order(sexp.v[0]) - 1

def strip_apps(sexp):
    if isinstance(sexp, Atom):
        return sexp
    if isinstance(sexp.v[0], Atom) and (sexp.v[0].char == '$' or sexp.v[0].char == '|'):
        return Cons(list(map(strip_apps, sexp.v[1:])))
    return Cons(list(map(strip_apps, sexp.v)))

def tests():
    def eq(input, sexp):
        out = str(strip_apps(parse(input)))
        assert(out == sexp)
    eq("1", "1")
    eq("1 + 2", "(+ 1 2)")
    eq("1 + 2 + 3", "(+ (+ 1 2) 3)")
    eq("1 + 2 * 3", "(+ 1 (* 2 3))")
    eq("-1", "(- 1)")
    eq("-1 + 3", "(+ (- 1) 3)")
    eq("3 + -1 + 4", "(+ (+ 3 (- 1)) 4)")
    eq("(3 + 1) + 4", "(+ (+ 3 1) 4)")
    eq("((3 + 1) + 4)", "(+ (+ 3 1) 4)")
    eq("(3 + 1) * 4", "(* (+ 3 1) 4)")
    eq("3 + (1 + 4)", "(+ 3 (+ 1 4))")
    eq("(1)(2)", "(* 1 2)")
    eq("(1)2", "(* 1 2)")
    eq("1(2)", "(* 1 2)")
    eq("--1", "(- (- 1))")
    eq("ab", "(* a b)")
    eq("f(x)", "(f x)")
    eq("(f)(x)", "(f x)")
    eq("(f + g)(x)", "((+ f g) x)")
    eq("x^2^3", "(^ x (^ 2 3))")
    eq("ax^2", "(* a (^ x 2))")
    eq("f$x", "(f x)")
    eq("Df(x)", "((D f) x)")
    eq("DDf(x)", "((D (D f)) x)")
    eq("D(f)(x)", "((D f) x)")
    eq("(((0)))", "0")
    eq("a(((0)))", "(* a 0)")
    eq("a(b + c)", "(* a (+ b c))")
    eq("D^2f(x)", "(((^ D 2) f) x)")

    # order()
    assert(order(Atom("D")) == 2)
    assert(order(Atom("f")) == 1)
    assert(order(Atom("1")) == 0)
    assert(order(Cons([Atom("+"), Atom("3"), Atom("1")])) == 0)
    assert(order(Cons([Atom("f"), Atom("1")])) == 0)
    assert(order(Cons([Atom("."), Atom("f"), Atom("g")])) == 1)
    assert(order(Cons([Atom("D"), Atom("f")])) == 1)
    assert(order(Cons([Cons([Atom("D"), Atom("f")]), Atom("1")])) == 0)
    print("\033[32mOK\033[39m")

tests()
