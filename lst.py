from typing import NamedTuple, List, Union

class Atom(NamedTuple):
    char: str
    def __repr__(self):
        return f'{self.char}'

class Lst(NamedTuple):
    v: List[Union['Atom', 'Lst']]
    def __repr__(self):
        return f'(' + ' '.join(map(str, self.v)) + ')'