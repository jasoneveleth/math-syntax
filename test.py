import sys

features = set()
if sys.argv[1] == 'infix':
    from infix import parse
    features.add('infix')
elif sys.argv[1] == 'prefix':
    from prefix import parse
    features.add('infix')
    features.add('prefix')
elif sys.argv[1] == 'juxt':
    from juxt import parse
    features.add('infix')
    features.add('prefix')
    features.add('juxt')
elif sys.argv[1] == 'paren':
    from paren import parse
    features.add('infix')
    features.add('prefix')
    features.add('juxt')
    features.add('paren')
else:
    print("must be `infix`, `prefix`, `juxt`, `paren`", file=sys.stderr)

def tests():
    def eq(input, sexp):
        out = str(parse(input))
        assert(out == sexp)
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
    # eq("a!", "(! a)")

    print("\033[32mOK\033[39m")

tests()

