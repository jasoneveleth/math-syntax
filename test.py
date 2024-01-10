import sys

def tests(parse, features):
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
            from infix import parse
            tests(parse, {'infix'})
        elif file == 'prefix':
            from prefix import parse
            tests(parse, {'infix', 'prefix'})
        elif file == 'juxt':
            from juxt import parse
            tests(parse, {'infix', 'prefix', 'juxt'})
        elif file == 'paren':
            from paren import parse
            tests(parse, {'infix', 'prefix', 'juxt', 'paren'})
        else:
            print(f"{file} must be `infix`, `prefix`, `juxt`, `paren`", file=sys.stderr)
            return 1
    return 0

exit(main())

