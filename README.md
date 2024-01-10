# Architecture

The following are Pratt parsers in increasing levels of expressiveness:

- `1-infix.py` just does infix
- `2-prefix.py` adds prefix parsing
- `3-juxt.py` adds implicit * juxtapose
- `4-paren.py` adds parethesis grouping and function application

They are meant to be looked at in order using `diff` to see the changes introduced.
I have spent a lot of time making it as intelligible as possible so hopefully no explanation
is necessary.

Run tests with `test.py`. It will print the commandline args it needs with `python test.py -h`.

Finally, `cons.py` has definitions of `Atom` and `Cons` which we build our syntax tree from (like lisp).

# Syntax

The return value from `parse` in each parser will stringify as an S-expression.
You might notice some strange operators in the output, like `$` and `|`.
Those are function and operator application.
You can remove them and get normal lispy S-expressions with `strip_apps()` in `test.py`.
The `sexp()` function in `test.py` will automatically do this.

If you want another stringification, checkout the `test.py` which also has RPN, python, and fully parenthesized syntax.

## missing:

- `:=` assignment (right assoc)
- `f(x,y)` functions of multiple args
- `>=` `>` `<` `<=` comparison
- `==` `!=` && || boolean operators
- `{1, 2, 3}` sets, vector `[1, 2, 3]`
- `\in \subset \union \intersection \difference \disjoint-union (or +)` set ops

- statements (function calls, assignment): everything else should be an expression.