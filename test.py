import sys
import importlib

def tests(parse, features):
    def eq(input, ans):
        out = sexp(parse(input))
        assert(out == ans)
    if 'infix' in features:
        eq("1", "1")
        eq("1 + 2", "(+ 1 2)")
        eq("1 + 2 + 3", "(+ (+ 1 2) 3)")
        eq("1 + 2 * 3", "(+ 1 (* 2 3))")
    if 'prefix' in features:
        eq("-1", "(- 1)")
        eq("-1 + 3", "(+ (- 1) 3)")
        eq("3 + -1 + 4", "(+ (+ 3 (- 1)) 4)")
    if 'juxt' in features:
        eq("ab", "(* a b)")
    if 'paren' in features:
        eq("(3 + 1) + 4", "(+ (+ 3 1) 4)")
        eq("((3 + 1) + 4)", "(+ (+ 3 1) 4)")
        eq("(3 + 1) * 4", "(* (+ 3 1) 4)")
        eq("3 + (1 + 4)", "(+ 3 (+ 1 4))")
        eq("(1)(2)", "(* 1 2)")
        eq("(1)2", "(* 1 2)")
        eq("1(2)", "(* 1 2)")
        eq("--1", "(- (- 1))")
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
        eq("f . g + h", "(+ (. f g) h)")
        eq("D(f . g)", "(D (. f g))")
        eq("Df . g", "(. (D f) g)")
    # eq("a!", "(! a)")

    print("\033[32mOK\033[39m")

def main():
    if len(sys.argv) == 1 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        yellow = "\033[33m"
        green = "\033[32m"
        done = "\033[39m"
        print(f"{yellow}USAGE:{done}")
        print(f"    python {sys.argv[0]} FILES")
        print()
        print(f"{yellow}FILES:{done}")
        print(f"    {green}infix{done}   use at least one of these")
        print(f"    {green}prefix{done}")
        print(f"    {green}juxt{done}")
        print(f"    {green}paren{done}")
        return 0

    for file in sys.argv[1:]:
        if file == 'infix':
            parse = importlib.import_module('1-infix').parse
            tests(parse, {'infix'})
        elif file == 'prefix':
            parse = importlib.import_module('2-prefix').parse
            tests(parse, {'infix', 'prefix'})
        elif file == 'juxt':
            parse = importlib.import_module('3-juxt').parse
            tests(parse, {'infix', 'prefix', 'juxt'})
        elif file == 'paren':
            parse = importlib.import_module('4-paren').parse
            tests(parse, {'infix', 'prefix', 'juxt', 'paren'})
        else:
            print(f"{file} must be `infix`, `prefix`, `juxt`, `paren`", file=sys.stderr)
            return 1
    return 0

# ===========
#  Stringify
# ===========

from lst import Atom, Lst

def strip_apps(exp):
    """strip out $ and | operators"""
    if isinstance(exp, Atom):
        return exp
    if isinstance(exp.v[0], Atom) and (exp.v[0].char == '$' or exp.v[0].char == '|'):
        return Lst(list(map(strip_apps, exp.v[1:])))
    return Lst(list(map(strip_apps, exp.v)))

def sexp(exp):
    return str(strip_apps(exp))

def rpn(exp):
    if isinstance(exp, Atom):
        return f'{exp.char}'
    return rpn(exp.v[1]) + ' ' + rpn(exp.v[2]) + ' ' + rpn(exp.v[0])

def fully_parenthesized(exp):
    def r(e):
        if isinstance(exp, Atom):
            return f'{e.char}'
        return '(' + r(e.v[1]) + ' ' + r(e.v[0]) + ' ' + r(e.v[2]) + ')'
    return r(exp)

def python_syntax(exp):
    pass

exit(main())
